# -----------------------------------------------------------
# Графический интерфейс предназначен для взаимодействия с БД
# объектов для ОПО нефтедобычи
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from pathlib import Path
from PySide2 import QtWidgets, QtGui


class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # Иконки
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        db_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        ok_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/ok.png')
        replace_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/replace.png')
        save_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
        clear_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/clear.png')
        del_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/del.png')
        question_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/question.png')
        scale_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/scale.png')
        dist_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/polyline.png')
        area_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/area.png')
        object_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/object.png')
        settings_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/settings.png')
        draw_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/draw.png')
        exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
        info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
        # Главное окно
        self.setGeometry(300, 300, 750, 550)
        self.setWindowTitle('Storage_app')
        self.setWindowIcon(self.main_ico)
        # Центральный виджет
        # создаем сетку из двух колонок
        # окно для графики
        # окно для ввода данных
        central_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(self)
        grid.setColumnStretch(0, 7)
        grid.setColumnStretch(1, 1)
        # В первой колонке создаем место под ген.план
        # создаем сцену  #создаем сцену и плосы прокрутки картинки
        self.scene = QtWidgets.QGraphicsScene(self)
        # создаем полосы прокрутки
        self.area = QtWidgets.QScrollArea(self)
        # добавляем картинку
        self.pixmap = QtGui.QPixmap()
        self.scene.addPixmap(self.pixmap)
        # создаем обработчик клика мыши по сцене
        # self.scene.mousePressEvent = self.m_press_event
        # создаем вид который визуализирует сцену
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.area.setWidget(self.view)
        self.area.setWidgetResizable(True)

        # т.к. данных  много создадим
        # вкладки табов
        self.tabs = QtWidgets.QTabWidget()  # создаем вкладки табов
        self.tab_main = QtWidgets.QWidget()  # 0. Главная вкладка с данными
        self.tab_settings = QtWidgets.QWidget()  # 1. Настройки
        # добавляем "0" таб на вкладку табов
        self.tabs.addTab(self.tab_main, "")  # 0. Главная вкладка с данными
        self.tabs.setTabIcon(0, draw_ico)
        self.tabs.setTabToolTip(0, "Главня вкладка")
        self.tab_main.layout = QtWidgets.QFormLayout(self)

        # Рамка №1 (то что будет в рамке 1)
        self.scale_name = QtWidgets.QLineEdit()
        self.scale_name.setPlaceholderText("Масштаб")
        self.scale_name.setToolTip("[м, пикс.]")
        self.scale_name.setReadOnly(True)

        # Рамка №2 (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox()  # д. проектируемый/существующий объект
        self.type_act.addItems(["Объект", "Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, object_ico)
        self.type_act.setItemIcon(1, scale_ico)
        self.type_act.setItemIcon(2, dist_ico)
        self.type_act.setItemIcon(3, area_ico)
        self.result_lbl = QtWidgets.QLabel()
        self.draw_btn = QtWidgets.QPushButton("Применить")
        self.draw_btn.setCheckable(True)
        self.draw_btn.setChecked(False)

        # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
        # т.к. элементы будут добавляться и их
        # потом нужно будет объединять в группы

        # Рамка №1
        layout_scale = QtWidgets.QFormLayout(self)
        GB_scale = QtWidgets.QGroupBox('Масштаб')
        GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_scale.addRow("", self.scale_name)
        GB_scale.setLayout(layout_scale)
        # Рамка №2
        layout_act = QtWidgets.QFormLayout(self)
        GB_act = QtWidgets.QGroupBox('Действие')
        GB_act.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_act.addRow("", self.type_act)
        layout_act.addRow("", self.draw_btn)
        layout_act.addRow("", self.result_lbl)
        GB_act.setLayout(layout_act)
        # Собираем рамки
        self.tab_main.layout.addWidget(GB_scale)
        self.tab_main.layout.addWidget(GB_act)
        # Размещаем на табе
        self.tab_main.setLayout(self.tab_main.layout)

        # добавляем "1" таб на вкладку табов
        self.tabs.addTab(self.tab_settings, "")  # 1. Настройки
        self.tabs.setTabIcon(1, settings_ico)
        self.tabs.setTabToolTip(1, "Настройки")
        self.tab_settings.layout = QtWidgets.QFormLayout(self)
        # Рамка №1 (то что будет в рамке 1)
        self.db_name = QtWidgets.QLineEdit()  # Наименование  базы данных
        self.db_name.setPlaceholderText("Наименование базы данных")
        self.db_name.setToolTip("Наименование базы данных")
        self.db_name.setReadOnly(True)
        # Рамка №2 (то что будет в рамке 2)
        self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов-- "])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        # self.plan_list.activated[str].connect(self.plan_list_select)

        # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
        # т.к. элементы будут добавляться и их
        # потом нужно будет объединять в группы
        # Рамка №1
        layout_db = QtWidgets.QFormLayout(self)
        GB_db = QtWidgets.QGroupBox('База данных')
        GB_db.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_db.addRow("", self.db_name)
        GB_db.setLayout(layout_db)
        # Рамка №2
        layout_plan = QtWidgets.QFormLayout(self)
        GB_plan = QtWidgets.QGroupBox('Ген.план')
        GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_plan.addRow("", self.plan_list)
        GB_plan.setLayout(layout_plan)
        # Размещаем на табе
        self.tab_settings.layout.addWidget(GB_db)
        self.tab_settings.layout.addWidget(GB_plan)
        # Размещаем на табе
        self.tab_settings.setLayout(self.tab_settings.layout)

        grid.addWidget(self.area, 0, 0, 1, 1)
        grid.addWidget(self.tabs, 0, 1, 1, 1)
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # База данных (меню)
        db_menu = QtWidgets.QMenu('База данных', self)
        db_create = QtWidgets.QAction(ok_ico, 'Создать', self)
        db_create.setStatusTip('Создать новую базу данных')
        db_create.triggered.connect(self.db_create)
        db_menu.addAction(db_create)
        db_connect = QtWidgets.QAction(db_ico, 'Подключиться', self)
        db_connect.setStatusTip('Подключиться к существующей базе данных')
        db_connect.triggered.connect(self.db_connect)
        db_menu.addAction(db_connect)

        # Генплан (меню)
        plan_menu = QtWidgets.QMenu('Ген.план', self)
        plan_add = QtWidgets.QAction(ok_ico, 'Добавить', self)
        plan_add.setStatusTip('Добавить новый план объекта')
        plan_add.setShortcut('Ctrl+N')
        plan_add.triggered.connect(self.plan_add)
        plan_menu.addAction(plan_add)
        plan_replace = QtWidgets.QAction(replace_ico, 'Заменить', self)
        plan_replace.setStatusTip('Заменить план объекта')
        plan_replace.setShortcut('Ctrl+R')
        plan_replace.triggered.connect(self.plan_replace)
        plan_menu.addAction(plan_replace)
        plan_save = QtWidgets.QAction(save_ico, 'Coхранить', self)
        plan_save.setStatusTip('Сохранить текущее изображение плана объекта как файл')
        plan_save.setShortcut('Ctrl+S')
        plan_save.triggered.connect(self.plan_save)
        plan_menu.addAction(plan_save)
        plan_clear = QtWidgets.QAction(clear_ico, 'Очистить', self)
        plan_clear.setStatusTip('Очистить план объекта')
        plan_clear.setShortcut('Ctrl+С')
        plan_clear.triggered.connect(self.plan_clear)
        plan_menu.addAction(plan_clear)
        plan_del = QtWidgets.QAction(del_ico, 'Удалить', self)
        plan_del.setStatusTip('Удалить изображение плана объекта')
        plan_del.setShortcut('Ctrl+X')
        plan_del.triggered.connect(self.plan_del)
        plan_menu.addAction(plan_del)

        # Выход из приложения
        exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_prog.setShortcut('Ctrl+Q')
        exit_prog.setStatusTip('Выход из Painter')
        exit_prog.triggered.connect(self.close_event)

        # Справка
        help_show = QtWidgets.QAction(question_ico, 'Справка', self)
        help_show.setShortcut('F1')
        help_show.setStatusTip('Открыть справку Painter')
        help_show.triggered.connect(self.help_show)

        # О приложении
        about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
        about_prog.setShortcut('F2')
        about_prog.setStatusTip('О приложении Painter')
        about_prog.triggered.connect(self.about_programm)

        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addMenu(db_menu)
        file_menu.addMenu(plan_menu)
        file_menu.addAction(exit_prog)
        help_menu = menubar.addMenu('Справка')
        help_menu.addAction(help_show)
        help_menu.addAction(about_prog)
        # Установить статусбар
        self.statusBar()

        # toolbar = self.addToolBar('Выход')
        # toolbar.addAction(exitAction)

        if not parent:
            self.show()

    # 1. Вкладка ФАЙЛ
    # Функции базы данных
    def db_connect(self):
        print("db_connect")

    def db_create(self):
        print("db_create")

    # Функции генплана
    def plan_add(self):
        print("plan_add")

    def plan_replace(self):
        print("plan_replace")

    def plan_save(self):
        print("plan_save")

    def plan_clear(self):
        print("plan_clear")

    def plan_del(self):
        print("plan_del")

    #     Функция выхода из программы
    def close_event(self) -> None:
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            "Выход из программы",
            "Выйти из программы?",
            (QtWidgets.QMessageBox.Yes
             | QtWidgets.QMessageBox.No)
        )
        messageBox.setButtonText(QtWidgets.QMessageBox.Yes, "Да")
        messageBox.setButtonText(QtWidgets.QMessageBox.No, "Нет")
        messageBox.setWindowIcon(self.main_ico)
        resultCode = messageBox.exec_()
        if resultCode == QtWidgets.QMessageBox.No:
            return
        elif resultCode == QtWidgets.QMessageBox.Yes:
            return self.close()


    # 2. Вкладка СПРАВКА
    # функция справки
    def help_show(self):
        print("help_show")

    #     Функция "О программе"
    def about_programm(self) -> None:
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Information,
            "О программе",
            """Программа <b>Painter</b>. Предназначена для отрисовки зон действия 
поражающих факторов и построения полей потенциального риска 
на основе данных из Excel. Разрабочик: <b>npfgsk.ru</b>""",
            (QtWidgets.QMessageBox.Ok)
        )
        messageBox.setWindowIcon(self.main_ico)
        messageBox.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Painter()
    app.exec_()