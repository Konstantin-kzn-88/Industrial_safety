from PySide2 import QtWidgets, QtGui, QtCore
import os
import sys
from pathlib import Path


class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # Иконки

        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/comp.png')
        tree_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tree.png')

        paint_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/painter.png')

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
        state_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/state.png')
        tube_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tube.png')
        tree_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tree.png')
        exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
        info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
        color_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/color_select.png')
        excel_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/excel.png')
        plus_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/plus.png')
        minus_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/minus.png')
        dbl_minus_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/double_minus.png')
        hand_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/hand.png')
        risk_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/risk.png')



        # Главное окно
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Safety_risk')
        self.setWindowIcon(self.main_ico)
        # Центральный виджет
        # создаем сетку из двух колонок
        # окно для дерева объектов и элементов рисования
        # окно для базыданных и кнопок
        central_widget = QtWidgets.QWidget()
        central_grid = QtWidgets.QGridLayout(self)
        central_grid.setColumnStretch(0, 1)
        central_grid.setColumnStretch(1, 7)
        central_grid.setRowStretch(0, 7)
        central_grid.setRowStretch(1, 1)

        # 1. Колонка "Дерево + панель рисования"
        # 1.1. Дерево объектов
        self.model = QtGui.QStandardItemModel(0, 0)  # Создаем модель QStandardItemModel для QTreeView
        self.all_items = QtGui.QStandardItem("Объекты:")  #
        self.all_items.setIcon(tree_ico)
        self.model.appendRow(self.all_items)
        self.view_tree = QtWidgets.QTreeView()
        self.view_tree.header().hide()
        self.view_tree.setModel(self.model)
        # self.view_tree.clicked.connect(self.treefunction)
        layout_tree = QtWidgets.QVBoxLayout(self)
        GB_tree = QtWidgets.QGroupBox('Дерево объектов')
        GB_tree.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_tree.addWidget(self.view_tree)
        GB_tree.setLayout(layout_tree)

        # 1.2. Панель рисования и инструментов
        # т.к. данных  много создадим
        # вкладки табов
        self.tabs = QtWidgets.QTabWidget()  # создаем вкладки табов
        self.tab_main = QtWidgets.QWidget()  # 0. Главная вкладка с данными
        self.tab_settings = QtWidgets.QWidget()  # 1. Настройки
        # добавляем "0" таб на вкладку табов
        self.tabs.addTab(self.tab_main, "")  # 0. Главная вкладка с данными
        self.tabs.setTabIcon(0, draw_ico)
        self.tabs.setTabToolTip(0, "Инструменты")
        self.tab_main.layout = QtWidgets.QFormLayout(self)

        # Рамка №1 (то что будет в рамке 1)
        self.scale_name = QtWidgets.QLineEdit()
        self.scale_name.setPlaceholderText("Масштаб")
        self.scale_name.setToolTip("В одном пикселе метров")
        # self.scale_name.setReadOnly(True)

        # Рамка №2 (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox()
        self.type_act.addItems(["Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, scale_ico)
        self.type_act.setItemIcon(1, dist_ico)
        self.type_act.setItemIcon(2, area_ico)
        # self.type_act.activated[str].connect(self.select_type_act)
        self.result_lbl = QtWidgets.QLabel()
        self.draw_btn = QtWidgets.QPushButton("Применить")
        # self.draw_btn.clicked.connect(self.change_draw_btn)
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
        self.tabs.setTabIcon(1, paint_ico)
        self.tabs.setTabToolTip(1, "Рисование")
        self.tab_settings.layout = QtWidgets.QFormLayout(self)
        # Рамка №1 (то что будет в рамке 1)
        self.db_name = QtWidgets.QLineEdit()  # Наименование  базы данных
        self.db_name.setPlaceholderText("Наименование базы данных")
        self.db_name.setToolTip("Наименование базы данных")
        self.db_name.setReadOnly(True)
        self.db_path = QtWidgets.QLineEdit()  # путь  базы данных
        self.db_path.setPlaceholderText("Путь базы данных")
        self.db_path.setToolTip("Путь базы данных")
        self.db_path.setReadOnly(True)
        # Рамка №2 (то что будет в рамке 2)
        self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов--"])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        # self.plan_list.activated[str].connect(self.plan_list_select)
        # Рамка №3 (то что будет в рамке 3)
        self.color_zone1_btn = QtWidgets.QPushButton("Зона 1")
        # self.color_zone1_btn.setIcon(color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        # self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QtWidgets.QPushButton("Зона 2")
        # self.color_zone2_btn.setIcon(color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QtWidgets.QPushButton("Зона 3")
        # self.color_zone3_btn.setIcon(color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QtWidgets.QPushButton("Зона 4")
        # self.color_zone4_btn.setIcon(color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QtWidgets.QPushButton("Зона 5")
        # self.color_zone5_btn.setIcon(color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QtWidgets.QPushButton("Зона 6")
        # self.color_zone6_btn.setIcon(color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.color_zone6_btn.clicked.connect(self.select_color)
        # Рамка №4 (то что будет в рамке 4)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)
        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        # self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        # self.get_data_btn.clicked.connect(self.get_data_excel)
        # Рамка №5 (то что будет в рамке 5)
        self.opacity = QtWidgets.QDoubleSpinBox()
        self.opacity.setDecimals(2)
        self.opacity.setRange(0, 1)
        self.opacity.setSingleStep(0.01)

        # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
        # т.к. элементы будут добавляться и их
        # потом нужно будет объединять в группы

        # Рамка №1
        layout_zone = QtWidgets.QFormLayout(self)
        GB_zone = QtWidgets.QGroupBox('Выбор цвета')
        GB_zone.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_1 = QtWidgets.QHBoxLayout()
        hbox_1.addWidget(self.color_zone1_btn)
        hbox_1.addWidget(self.color_zone2_btn)
        layout_zone.addRow("", hbox_1)
        hbox_2 = QtWidgets.QHBoxLayout()
        hbox_2.addWidget(self.color_zone3_btn)
        hbox_2.addWidget(self.color_zone4_btn)
        layout_zone.addRow("", hbox_2)
        hbox_3 = QtWidgets.QHBoxLayout()
        hbox_3.addWidget(self.color_zone5_btn)
        hbox_3.addWidget(self.color_zone6_btn)
        layout_zone.addRow("", hbox_3)
        GB_zone.setLayout(layout_zone)
        # Рамка №2
        layout_xl = QtWidgets.QFormLayout(self)
        GB_xl = QtWidgets.QGroupBox('Данные из Excel')
        GB_xl.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_xl.addRow("", self.data_excel)
        layout_xl.addRow("", self.get_data_btn)
        GB_xl.setLayout(layout_xl)
        # Рамка №3
        layout_opacity = QtWidgets.QFormLayout(self)
        GB_opacity = QtWidgets.QGroupBox('Прозрачность')
        GB_opacity.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_opacity.addRow("", self.opacity)
        GB_opacity.setLayout(layout_opacity)

        # Размещаем на табе
        self.tab_settings.layout.addWidget(GB_zone)
        self.tab_settings.layout.addWidget(GB_xl)
        self.tab_settings.layout.addWidget(GB_opacity)
        # Размещаем на табе
        self.tab_settings.setLayout(self.tab_settings.layout)

        # 2. Колонка "Карта + таблица данных"
        # 2.1. В второй колонке создаем место под ген.план
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

        # 2.2. Таблица данных
        self.table_data = QtWidgets.QTableWidget(10, 10)
        header_item = QtWidgets.QTableWidgetItem("Foo")
        self.table_data.setHorizontalHeaderItem(1, header_item)






        central_grid.addWidget(GB_tree, 0, 0, 1, 1)
        central_grid.addWidget(self.area, 0, 1, 1, 1)
        central_grid.addWidget(self.tabs, 1, 0, 1, 1)
        central_grid.addWidget(self.table_data, 1, 1, 1, 1)
        central_widget.setLayout(central_grid)
        self.setCentralWidget(central_widget)

        # 3. Меню (тулбар)
        # База данных (меню)
        db_menu = QtWidgets.QMenu('База данных', self)
        db_create = QtWidgets.QAction(ok_ico, 'Создать', self)
        db_create.setStatusTip('Создать новую базу данных')
        # db_create.triggered.connect(self.db_create)
        db_menu.addAction(db_create)
        db_connect = QtWidgets.QAction(db_ico, 'Подключиться', self)
        db_connect.setStatusTip('Подключиться к существующей базе данных')
        # db_connect.triggered.connect(self.db_connect)
        db_menu.addAction(db_connect)

        # Генплан (меню)
        plan_menu = QtWidgets.QMenu('Ген.план', self)
        plan_add = QtWidgets.QAction(ok_ico, 'Добавить', self)
        plan_add.setStatusTip('Добавить новый план объекта')
        plan_add.setShortcut('Ctrl+N')
        # plan_add.triggered.connect(self.plan_add)
        plan_menu.addAction(plan_add)
        plan_replace = QtWidgets.QAction(replace_ico, 'Заменить', self)
        plan_replace.setStatusTip('Заменить план объекта')
        plan_replace.setShortcut('Ctrl+R')
        # plan_replace.triggered.connect(self.plan_replace)
        plan_menu.addAction(plan_replace)
        plan_save = QtWidgets.QAction(save_ico, 'Coхранить', self)
        plan_save.setStatusTip('Сохранить текущее изображение плана объекта как файл')
        plan_save.setShortcut('Ctrl+S')
        # plan_save.triggered.connect(self.plan_save)
        plan_menu.addAction(plan_save)
        plan_clear = QtWidgets.QAction(clear_ico, 'Очистить', self)
        plan_clear.setStatusTip('Очистить план объекта')
        plan_clear.setShortcut('Ctrl+С')
        # plan_clear.triggered.connect(self.plan_clear)
        plan_menu.addAction(plan_clear)
        plan_del = QtWidgets.QAction(del_ico, 'Удалить план с объектами', self)
        plan_del.setStatusTip('Удалить изображение плана объекта')
        plan_del.setShortcut('Ctrl+X')
        # plan_del.triggered.connect(self.plan_del)
        # plan_menu.addAction(plan_del)

        # Выход из приложения
        exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_prog.setShortcut('Ctrl+Q')
        exit_prog.setStatusTip('Выход из Painter')
        # exit_prog.triggered.connect(self.close_event)

        # Вид +/- и "рука"
        scale_plus = QtWidgets.QAction(plus_ico, 'Увеличить план', self)
        scale_plus.setShortcut('Ctrl+P')
        scale_plus.setStatusTip('Увеличить план')
        # scale_plus.triggered.connect(self.scale_view_plus)

        scale_min = QtWidgets.QAction(minus_ico, 'Уменьшить план', self)
        scale_min.setShortcut('Ctrl+M')
        scale_min.setStatusTip('Уменьшить план')
        # scale_min.triggered.connect(self.scale_view_min)

        hand_act = QtWidgets.QAction(hand_ico, 'Рука', self)
        hand_act.setShortcut('Ctrl+H')
        hand_act.setStatusTip('Рука')
        # hand_act.triggered.connect(self.plan_hand)

        # # Редактировать объект
        del_end_point = QtWidgets.QAction(minus_ico, 'Удалить последнюю точку', self)
        del_end_point.setShortcut('Ctrl+D')
        del_end_point.setStatusTip('Удалить последнюю точку')
        # del_end_point.triggered.connect(self.delete_end_point)

        del_all_point = QtWidgets.QAction(dbl_minus_ico, 'Удалить все точки', self)
        del_all_point.setShortcut('Ctrl+A')
        del_all_point.setStatusTip('Удалить все точки')
        # del_all_point.triggered.connect(self.delete_all_point)

        save_obj = QtWidgets.QAction(save_ico, 'Сохранить', self)
        save_obj.setShortcut('Ctrl+W')
        save_obj.setStatusTip('Сохранить объект')
        # save_obj.triggered.connect(self.save_object)

        del_obj = QtWidgets.QAction(del_ico, 'Удалить', self)
        del_obj.setShortcut('Ctrl+R')
        del_obj.setStatusTip('Удалить объект')
        # del_obj.triggered.connect(self.on_del_object)

        # Рисование объекта
        draw_all = QtWidgets.QAction(self.main_ico, 'Все объекты', self)
        draw_all.setStatusTip('Рисовать все объекты')
        # draw_all.triggered.connect(self.draw_all_object)

        draw_one = QtWidgets.QAction(object_ico, 'Один объект', self)
        draw_one.setStatusTip('Рисовать один объект')
        # draw_one.triggered.connect(self.draw_one_object)

        draw_risk = QtWidgets.QAction(risk_ico, 'Риск', self)
        draw_risk.setStatusTip('Рисовать риск')
        # draw_risk.triggered.connect(self.draw_risk_object)

        # Справка
        help_show = QtWidgets.QAction(question_ico, 'Справка', self)
        help_show.setShortcut('F1')
        help_show.setStatusTip('Открыть справку Painter')
        # help_show.triggered.connect(self.help_show)

        # О приложении
        about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
        about_prog.setShortcut('F2')
        about_prog.setStatusTip('О приложении Painter')
        # about_prog.triggered.connect(self.about_programm)

        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addMenu(db_menu)
        file_menu.addMenu(plan_menu)
        file_menu.addAction(exit_prog)
        view_menu = menubar.addMenu('Вид')
        view_menu.addAction(scale_plus)
        view_menu.addAction(scale_min)
        view_menu.addAction(hand_act)
        edit_menu = menubar.addMenu('Объект')
        edit_menu.addAction(del_end_point)
        edit_menu.addAction(del_all_point)
        edit_menu.addAction(save_obj)
        edit_menu.addAction(del_obj)
        draw_menu = menubar.addMenu('Рисование')
        draw_menu.addAction(draw_all)
        draw_menu.addAction(draw_one)
        draw_menu.addAction(draw_risk)
        help_menu = menubar.addMenu('Справка')
        help_menu.addAction(help_show)
        help_menu.addAction(about_prog)
        # Установить статусбар
        self.statusBar()




        if not parent:
            self.show()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Painter()
    app.exec_()