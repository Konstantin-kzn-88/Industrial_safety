from PySide2 import QtWidgets, QtGui, QtCore
import os
import sys
from pathlib import Path

class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # Иконки
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/painter.png')
        tree_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tree.png')

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
        # self.tabs.setTabIcon(0, draw_ico)
        self.tabs.setTabToolTip(0, "Главня вкладка")
        self.tab_main.layout = QtWidgets.QFormLayout(self)

        # Рамка №1 (то что будет в рамке 1)
        self.scale_name = QtWidgets.QLineEdit()
        self.scale_name.setPlaceholderText("Масштаб")
        self.scale_name.setToolTip("В одном пикселе метров")
        # self.scale_name.setReadOnly(True)

        # Рамка №2 (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox()
        self.type_act.addItems(["Объект", "Масштаб", "Расстояние", "Площадь"])
        # self.type_act.setItemIcon(0, object_ico)
        # self.type_act.setItemIcon(1, scale_ico)
        # self.type_act.setItemIcon(2, dist_ico)
        # self.type_act.setItemIcon(3, area_ico)
        # self.type_act.activated[str].connect(self.select_type_act)
        self.result_lbl = QtWidgets.QLabel()
        self.draw_btn = QtWidgets.QPushButton("Применить")
        # self.draw_btn.clicked.connect(self.change_draw_btn)
        self.draw_btn.setCheckable(True)
        self.draw_btn.setChecked(False)

        # Рамка №3 (то что будет в рамке 3)
        self.obj_name = QtWidgets.QLineEdit()
        self.obj_name.setPlaceholderText("Наименование объекта")
        self.obj_name.setToolTip("Е-1")
        self.obj_coord = QtWidgets.QLineEdit()
        self.obj_coord.setPlaceholderText("Координаты объекта")
        self.obj_coord.setToolTip("[x,y]")
        self.obj_coord.setReadOnly(True)
        self.obj_type = QtWidgets.QComboBox()
        self.obj_type.addItems(["Линейный", "Стационарный"])
        # self.obj_type.setItemIcon(0, tube_ico)
        # self.obj_type.setItemIcon(1, state_ico)

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
        # Рамка №3
        layout_obj = QtWidgets.QFormLayout(self)
        GB_obj = QtWidgets.QGroupBox('Объект')
        GB_obj.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_obj.addRow("", self.obj_name)
        layout_obj.addRow("", self.obj_coord)
        layout_obj.addRow("", self.obj_type)
        GB_obj.setLayout(layout_obj)

        # Собираем рамки
        self.tab_main.layout.addWidget(GB_scale)
        self.tab_main.layout.addWidget(GB_act)
        self.tab_main.layout.addWidget(GB_obj)

        # Размещаем на табе
        self.tab_main.setLayout(self.tab_main.layout)

        # добавляем "1" таб на вкладку табов
        self.tabs.addTab(self.tab_settings, "")  # 1. Настройки
        # self.tabs.setTabIcon(1, settings_ico)
        self.tabs.setTabToolTip(1, "Настройки")
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
        layout_db = QtWidgets.QFormLayout(self)
        GB_db = QtWidgets.QGroupBox('База данных')
        GB_db.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_db.addRow("", self.db_name)
        layout_db.addRow("", self.db_path)
        GB_db.setLayout(layout_db)
        # Рамка №2
        layout_plan = QtWidgets.QFormLayout(self)
        GB_plan = QtWidgets.QGroupBox('Ген.план')
        GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_plan.addRow("", self.plan_list)
        GB_plan.setLayout(layout_plan)
        # Рамка №3
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
        # Рамка №4
        layout_xl = QtWidgets.QFormLayout(self)
        GB_xl = QtWidgets.QGroupBox('Данные из Excel')
        GB_xl.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_xl.addRow("", self.data_excel)
        layout_xl.addRow("", self.get_data_btn)
        GB_xl.setLayout(layout_xl)
        # Рамка №5
        layout_opacity = QtWidgets.QFormLayout(self)
        GB_opacity = QtWidgets.QGroupBox('Прозрачность')
        GB_opacity.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_opacity.addRow("", self.opacity)
        GB_opacity.setLayout(layout_opacity)

        # Размещаем на табе
        self.tab_settings.layout.addWidget(GB_db)
        self.tab_settings.layout.addWidget(GB_plan)
        self.tab_settings.layout.addWidget(GB_zone)
        self.tab_settings.layout.addWidget(GB_xl)
        self.tab_settings.layout.addWidget(GB_opacity)
        # Размещаем на табе
        self.tab_settings.setLayout(self.tab_settings.layout)

        # 2. Колонка "Карта + база данных"
        # В второй колонке создаем место под ген.план
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


        central_grid.addWidget(GB_tree, 0, 0, 1, 1)
        central_grid.addWidget(self.area, 0, 1, 1, 1)
        central_grid.addWidget(self.tabs, 1, 0, 1, 1)
        central_widget.setLayout(central_grid)
        self.setCentralWidget(central_widget)

        if not parent:
            self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Painter()
    app.exec_()