# -----------------------------------------------------------
# Графический интерфейс предназначен для взаимодействия с БД
# объектов для ОПО нефтедобычи
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from pathlib import Path
from PySide2 import QtWidgets, QtGui, QtSql

db = QtSql.QSqlDatabase("QSQLITE")
db.setDatabaseName("data.db")
db.open()

class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # Иконки
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        company_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/company.png')
        state_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/state.png')
        ok_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/ok.png')
        object_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/object.png')
        doc_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/document.png')
        line_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tube.png')






        replace_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/replace.png')
        save_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
        clear_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/clear.png')
        # del_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/del.png')
        question_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/question.png')
        scale_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/scale.png')
        dist_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/polyline.png')
        area_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/area.png')
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
        grid.setColumnStretch(0, 5)
        grid.setColumnStretch(1, 2)
        # В первой колонке создаем место под вид БД
        self.table = QtWidgets.QTableView()
        self.model = QtSql.QSqlRelationalTableModel(db=db)
        self.table.setModel(self.model)
        self.model.setTable("company")

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

        grid.addWidget(self.table, 0, 0, 1, 1)
        grid.addWidget(self.tabs, 0, 1, 1, 1)
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # База данных (меню)
        main_menu = QtWidgets.QMenu('База данных', self)
        file_is_open = QtWidgets.QAction(ok_ico, 'Подключение', self)
        file_is_open.setStatusTip('Подключиться к базе данных')
        file_is_open.triggered.connect(self.file_is_open)
        main_menu.addAction(file_is_open)

        # Формы добавления информации в БД (меню)
        add_menu = QtWidgets.QMenu('Информация в базу данных', self)
        company_add = QtWidgets.QAction(company_ico, 'Добавить компанию', self)
        company_add.setStatusTip('Добавить новую компанию')
        # company_add.triggered.connect(self.company_add)
        add_menu.addAction(company_add)
        opo_add = QtWidgets.QAction(object_ico, 'Добавить ОПО', self)
        opo_add.setStatusTip('Добавить новый опасный производственный объект')
        # opo_add.triggered.connect(self.company_add)
        add_menu.addAction(opo_add)
        doc_add = QtWidgets.QAction(doc_ico, 'Добавить документацию объекта', self)
        doc_add.setStatusTip('Добавить документацию опасного производственного объекта')
        # doc_add.triggered.connect(self.company_add)
        add_menu.addAction(doc_add)
        line_obj_add = QtWidgets.QAction(line_ico, 'Добавить линейный объект', self)
        line_obj_add.setStatusTip('Добавить линейный объект')
        # doc_add.triggered.connect(self.company_add)
        add_menu.addAction(line_obj_add)
        state_obj_add = QtWidgets.QAction(state_ico, 'Добавить стационарный объект', self)
        state_obj_add.setStatusTip('Добавить новый стационарный объект')
        # company_add.triggered.connect(self.company_add)
        add_menu.addAction(state_obj_add)

        # Выход из приложения
        exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_prog.setShortcut('Ctrl+Q')
        exit_prog.setStatusTip('Выход из Storage_app')
        exit_prog.triggered.connect(self.close_event)

        # Справка
        help_show = QtWidgets.QAction(question_ico, 'Справка', self)
        help_show.setShortcut('F1')
        help_show.setStatusTip('Открыть справку Storage_app')
        help_show.triggered.connect(self.help_show)

        # О приложении
        about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
        about_prog.setShortcut('F2')
        about_prog.setStatusTip('О приложении Storage_app')
        about_prog.triggered.connect(self.about_programm)

        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addMenu(main_menu)
        file_menu.addAction(exit_prog)
        db_menu = menubar.addMenu('База данных')
        db_menu.addMenu(add_menu)
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
    def file_is_open(self):
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            "Соединение с базой данных",
            "Соединение с базой данных проверяется"
            "только для серверных баз данных",
            (QtWidgets.QMessageBox.Ok)
        )
        messageBox.setWindowIcon(self.main_ico)
        resultCode = messageBox.exec_()
        if resultCode == QtWidgets.QMessageBox.Ok:
            return


    # Функции добавления в БД
    def company_add(self):
        print("company_add")

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
            """Программа <b>Storage_app</b>. Предназначена для хранения данных об опасных производственных объектах.
Разрабочик: <b>npfgsk.ru</b>""",
            (QtWidgets.QMessageBox.Ok)
        )
        messageBox.setWindowIcon(self.main_ico)
        messageBox.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = Storage_app()
    app.exec_()