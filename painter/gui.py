# -----------------------------------------------------------
# Графический интерфейс предназначен для отрисовки зон действия
# поражающих факторов и построения полей потенциального риска
# на основе данных из excel (расчеты в данном модуле не производятся)
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import json
import math
import sqlite3
import time
import sys
import os
from pathlib import Path

import numpy as np
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QTranslator
from shapely.geometry import Point, LineString, Polygon
import win32com.client
import matplotlib.pyplot as plt

Excel = win32com.client.Dispatch("Excel.Application")

I18N_QT_PATH = str(os.path.join(os.path.abspath('.'), 'i18n'))


class MoveItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__()
        self.tag = None

    def boundingRect(self):
        # print('boundingRect')
        return QtCore.QRectF(-10, -10, 10, 10);

    def paint(self, painter, option, widget):  # рисуем новый квадрат со стороной 10
        # print('paint')
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(-5, -5, 5, 5)


class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # Иконки
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/painter.png')
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
        # Важные переменные и объекты
        self.scale = 1  # изначально масштаб картинки 1
        self.data_scale = []  # массив хранения данных для масштаба
        self.data_point = []  # массив для хранения точек (измерение дистанции и площади)
        self.data_obj = {}  # словарь всех объектов
        self.last_risk_arr = None

        # Главное окно
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Painter')
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
        self.scene.mousePressEvent = self.scene_press_event
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
        self.scale_name.setToolTip("В одном пикселе метров")
        # self.scale_name.setReadOnly(True)

        # Рамка №2 (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox()
        self.type_act.addItems(["Объект", "Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, object_ico)
        self.type_act.setItemIcon(1, scale_ico)
        self.type_act.setItemIcon(2, dist_ico)
        self.type_act.setItemIcon(3, area_ico)
        self.type_act.activated[str].connect(self.select_type_act)
        self.result_lbl = QtWidgets.QLabel()
        self.draw_btn = QtWidgets.QPushButton("Применить")
        self.draw_btn.clicked.connect(self.change_draw_btn)
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
        self.obj_type.setItemIcon(0, tube_ico)
        self.obj_type.setItemIcon(1, state_ico)

        # Рамка №4 (то что будет в рамке 4)
        self.model = QtGui.QStandardItemModel(0, 0)  # Создаем модель QStandardItemModel для QTreeView
        self.all_items = QtGui.QStandardItem("Объекты:")  #
        self.all_items.setIcon(tree_ico)
        self.model.appendRow(self.all_items)
        self.view_tree = QtWidgets.QTreeView()
        self.view_tree.header().hide()
        self.view_tree.setModel(self.model)
        self.view_tree.clicked.connect(self.treefunction)

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
        # Рамка №4
        layout_tree = QtWidgets.QVBoxLayout(self)
        GB_tree = QtWidgets.QGroupBox('Дерево объектов')
        GB_tree.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_tree.addWidget(self.view_tree)
        GB_tree.setLayout(layout_tree)
        # Собираем рамки
        self.tab_main.layout.addWidget(GB_scale)
        self.tab_main.layout.addWidget(GB_act)
        self.tab_main.layout.addWidget(GB_obj)
        self.tab_main.layout.addWidget(GB_tree)
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
        self.db_path = QtWidgets.QLineEdit()  # путь  базы данных
        self.db_path.setPlaceholderText("Путь базы данных")
        self.db_path.setToolTip("Путь базы данных")
        self.db_path.setReadOnly(True)
        # Рамка №2 (то что будет в рамке 2)
        self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов--"])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        self.plan_list.activated[str].connect(self.plan_list_select)
        # Рамка №3 (то что будет в рамке 3)
        self.color_zone1_btn = QtWidgets.QPushButton("Зона 1")
        self.color_zone1_btn.setIcon(color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QtWidgets.QPushButton("Зона 2")
        self.color_zone2_btn.setIcon(color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QtWidgets.QPushButton("Зона 3")
        self.color_zone3_btn.setIcon(color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QtWidgets.QPushButton("Зона 4")
        self.color_zone4_btn.setIcon(color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QtWidgets.QPushButton("Зона 5")
        self.color_zone5_btn.setIcon(color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QtWidgets.QPushButton("Зона 6")
        self.color_zone6_btn.setIcon(color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        self.color_zone6_btn.clicked.connect(self.select_color)
        # Рамка №4 (то что будет в рамке 4)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)
        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        self.get_data_btn.clicked.connect(self.get_data_excel)
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
        plan_del = QtWidgets.QAction(del_ico, 'Удалить план с объектами', self)
        plan_del.setStatusTip('Удалить изображение плана объекта')
        plan_del.setShortcut('Ctrl+X')
        plan_del.triggered.connect(self.plan_del)
        plan_menu.addAction(plan_del)

        # Выход из приложения
        exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_prog.setShortcut('Ctrl+Q')
        exit_prog.setStatusTip('Выход из Painter')
        exit_prog.triggered.connect(self.close_event)

        # Вид +/- и "рука"
        scale_plus = QtWidgets.QAction(plus_ico, 'Увеличить план', self)
        scale_plus.setShortcut('Ctrl+P')
        scale_plus.setStatusTip('Увеличить план')
        scale_plus.triggered.connect(self.scale_view_plus)

        scale_min = QtWidgets.QAction(minus_ico, 'Уменьшить план', self)
        scale_min.setShortcut('Ctrl+M')
        scale_min.setStatusTip('Уменьшить план')
        scale_min.triggered.connect(self.scale_view_min)

        hand_act = QtWidgets.QAction(hand_ico, 'Рука', self)
        hand_act.setShortcut('Ctrl+H')
        hand_act.setStatusTip('Рука')
        hand_act.triggered.connect(self.plan_hand)

        # # Редактировать объект
        del_end_point = QtWidgets.QAction(minus_ico, 'Удалить последнюю точку', self)
        del_end_point.setShortcut('Ctrl+D')
        del_end_point.setStatusTip('Удалить последнюю точку')
        del_end_point.triggered.connect(self.delete_end_point)

        del_all_point = QtWidgets.QAction(dbl_minus_ico, 'Удалить все точки', self)
        del_all_point.setShortcut('Ctrl+A')
        del_all_point.setStatusTip('Удалить все точки')
        del_all_point.triggered.connect(self.delete_all_point)

        save_obj = QtWidgets.QAction(save_ico, 'Сохранить', self)
        save_obj.setShortcut('Ctrl+W')
        save_obj.setStatusTip('Сохранить объект')
        save_obj.triggered.connect(self.save_object)

        del_obj = QtWidgets.QAction(del_ico, 'Удалить', self)
        del_obj.setShortcut('Ctrl+R')
        del_obj.setStatusTip('Удалить объект')
        del_obj.triggered.connect(self.on_del_object)

        # Рисование объекта
        draw_all = QtWidgets.QAction(self.main_ico, 'Все объекты', self)
        draw_all.setStatusTip('Рисовать все объекты')
        draw_all.triggered.connect(self.draw_all_object)

        draw_one = QtWidgets.QAction(object_ico, 'Один объект', self)
        draw_one.setStatusTip('Рисовать один объект')
        draw_one.triggered.connect(self.draw_one_object)

        draw_risk = QtWidgets.QAction(risk_ico, 'Риск', self)
        draw_risk.setStatusTip('Рисовать риск')
        draw_risk.triggered.connect(self.draw_risk_object)

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

        # toolbar = self.addToolBar('Выход')
        # toolbar.addAction(exitAction)

        if not parent:
            self.show()

    # 1. Вкладка ФАЙЛ
    # Функции базы данных
    def db_connect(self):
        """
        Подключение к существующей БД
        """

        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть базу данных', "/home", ("Data base (*.db)"))[0]
        if path == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Файл базы данных не выбран")
            msg.exec()
            return
        file_name = QtCore.QFileInfo(path).fileName()
        file_path = QtCore.QFileInfo(path).path()
        self.db_name.setText(file_name)
        self.db_path.setText(file_path)
        self.plan_list_update()

    def db_create(self):
        """
         Функция содает новую БД и сохраняет ее в папке
         """
        text, ok = QtWidgets.QInputDialog.getText(self, 'Создать новую базу данных', 'Введите имя новой базы данных:')
        # self.vibor_master_plan.clear() #очистить ген.план.

        if ok:
            # получить путь сохранения базы данных
            dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать путь базы данных",
                                                             "/home",
                                                             QtWidgets.QFileDialog.ShowDirsOnly
                                                             | QtWidgets.QFileDialog.DontResolveSymlinks)
            # проверить нет ли такого же файла в той же директории
            check = os.path.exists(f"{dir}/{text}.db")
            if check:
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText("База данных с таким названием уже существует!")
                msg.exec()
                return
            sqliteConnection = sqlite3.connect(f"{dir}/{text}.db")
            cursorObj = sqliteConnection.cursor()
            cursorObj.execute("""CREATE TABLE objects(id INTEGER PRIMARY KEY, data TEXT NOT NULL,
                                                                 photo BLOB NOT NULL, name_photo TEXT NOT NULL)""")
            sqliteConnection.commit()
            sqliteConnection.close
            self.db_name.setText(text + '.db')
            self.db_path.setText(dir)
        else:
            return

    # Функции генплана
    def plan_add(self):
        """
         Загрузка файла картинки
        """
        # Проверка подключения к базе данных
        # проверка базы данных
        if self.is_there_a_database() == False:
            return

        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть генеральный план',
                                                          "/home", ("Images (*.jpg)"))[0]
        # Проверка выбран ли файл ген.плана
        if file_path == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Файл не выбран")
            msg.exec()
            return

        file_name = QtCore.QFileInfo(file_path).fileName()
        # Подключение к базе данных
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        real_id = cursorObj.fetchall()
        # проверка максимального id в базе
        max_id = 1
        if real_id == []:
            max_id = 1
        else:
            for row in real_id:
                max_id = int(row[0]) + 1
                print(max_id)

        # SQL запрос
        sqlite_insert_blob_query = """ INSERT INTO 'objects'
                                            ('id', 'data', 'photo', 'name_photo') VALUES (?, ?, ?, ?)"""
        # Конвертация файла в BLOB
        empPhoto = self.convertToBinaryData(file_path)
        # Проготовим множество к вставке в SQL запрос
        data_tuple = (max_id, "", empPhoto, file_name)
        cursorObj.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        cursorObj.close()
        self.plan_list_update()

    def plan_replace(self):
        # проверка базы данных
        if self.is_there_a_database() == False:
            return

        file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть генеральный план',
                                                          "/home", ("Images (*.jpg)"))[0]
        # Проверка выбран ли файл ген.плана
        if file_path == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Файл не выбран")
            msg.exec()
            return
        file_name = QtCore.QFileInfo(file_path).fileName()
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()

        cursorObj.execute("SELECT * FROM objects")
        real_id = cursorObj.fetchall()

        if real_id == []:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Ген.плана еще нет, поэтому его замена не возможна")
            msg.exec()
            return
        else:
            for row in real_id:
                if str(row[3]) + ',' + str(row[0]) == self.plan_list.currentText():
                    print("Hey")
                    empPhoto = self.convertToBinaryData(file_path)
                    cursorObj.execute('UPDATE objects SET photo = ?  where id = ?', (empPhoto, str(row[0])))
                    cursorObj.execute('UPDATE objects SET name_photo = ? where id = ?', (file_name, str(row[0])))
                    sqliteConnection.commit()
                    print("Image and file replaced successfully as a BLOB into a table")
                    cursorObj.close()
        self.plan_list_update()
        self.scene.clear()

    def plan_save(self):
        """
        Сохранение текущего вида ген.плана
        """
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        text = str(int(time.time()))
        # self.del_all_item()
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QtGui.QImage(self.scene.sceneRect().size().toSize(), QtGui.QImage.Format_ARGB32)
        image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        image.save((f"{self.db_path.text()}/{text}.jpg"), "JPG")
        painter.end()

    def plan_clear(self):
        # очистить ген.план от разных зон и объектов
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        self.plan_list_select(text=self.plan_list.currentText())

    def plan_del(self):
        """
        Удаление ген.плана из БД
        """
        if self.db_name.text() == '':
            return
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()

        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        for row in plant_in_db:

            if str(row[3]) + ',' + str(row[0]) == self.plan_list.currentText():
                sql = 'DELETE FROM objects WHERE id=?'
                cursorObj.execute(sql, (str(row[0]),))

                sqliteConnection.commit()
                sqliteConnection.execute("VACUUM")
                cursorObj.close()
        self.plan_list_update()
        self.scene.clear()

    def convertToBinaryData(self, file_path):
        # Конвертирование в BLOB
        with open(file_path, 'rb') as file:
            blobData = file.read()
        return blobData

    def plan_list_select(self, text):
        """
        Выбор ген.плана из QCombobox
        """
        # очистить поля
        self.zeroing_object()
        # достаем картинку из БД
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        for row in plant_in_db:
            if str(row[3]) + ',' + str(row[0]) == text:
                image_data = row[2]
                self.scene.clear()
                qimg = QtGui.QImage.fromData(image_data)
                self.pixmap = QtGui.QPixmap.fromImage(qimg)
                self.scene.addPixmap(self.pixmap)
                self.scene.setSceneRect(QtCore.QRectF(self.pixmap.rect()))
        sqliteConnection.execute("VACUUM")
        cursorObj.close()

        # Очищаем словарь объектов
        self.data_obj.clear()
        # достаем словарь из БД
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        data_in_db = cursorObj.fetchall()
        for row in data_in_db:
            if str(row[3]) + ',' + str(row[0]) == text:
                if str(row[1]) == "":
                    self.data_obj = {}
                else:
                    self.data_obj = eval(row[1])
        sqliteConnection.execute("VACUUM")
        cursorObj.close()
        # Удаляем все позиции из объектов
        self.all_items.removeRows(0, self.all_items.rowCount())
        # добавить из списка self.data_obj  объекты
        for key in self.data_obj.keys():
            key = QtGui.QStandardItem(key)
            self.all_items.setChild(self.all_items.rowCount(), key)

    def plan_list_update(self):
        """
        Обновление списка ген.планов по базе данных
        """
        # подключение к базе данных
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        self.plan_list.clear()

        plan_item = []

        for row in plant_in_db:
            name_plant = str(row[3]) + ',' + str(row[0])
            plan_item.append(name_plant)
        if plan_item == []:
            self.plan_list.addItems(["--Нет ген.планов-- "])
        else:
            self.plan_list.addItems(plan_item)
        sqliteConnection.execute("VACUUM")
        cursorObj.close()
        print("update plan")

    # Функции работы с ген.планом
    def scene_press_event(self, event):  # функция клика по ген.плану
        # Проверим наличие ген.плана
        if self.is_there_a_plan() == False:
            return
        # Проверим нажатие кнопки и действия QCombobox:
        if self.draw_btn.isChecked():
            if self.type_act.currentIndex() == 0:
                self.del_all_item()  # удалим все Item
                if self.scale_name.text() == "":  # проверим есть ли масштаб
                    msg = QtWidgets.QMessageBox(self)
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Информация")
                    msg.setText("Не установлен масштаб")
                    msg.exec()
                    self.draw_btn.setChecked(False)
                    return
                if self.obj_coord.displayText() == "":
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                else:
                    self.data_point = json.loads(self.obj_coord.displayText())
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                self.draw_all_item(json.loads(self.obj_coord.displayText()))

            elif self.type_act.currentIndex() == 1:
                # Вычислить масштаб
                self.data_scale.append(str(event.scenePos().x()))  # замеряем координаты клика
                self.data_scale.append(str(event.scenePos().y()))  # и запсываем в data_scale
                self.draw_all_item(self.data_scale)

                if len(self.data_scale) == 4:  # как только длина data_scale == 4
                    num_int, ok = QtWidgets.QInputDialog.getInt(self, "Масштаб", "Сколько метров:")
                    if ok:
                        x_a = float(self.data_scale[0])  # по координатам двух точек
                        y_a = float(self.data_scale[1])  # вычисляем расстояние в пикселях
                        x_b = float(self.data_scale[2])
                        y_b = float(self.data_scale[3])

                        length = LineString([(x_a, y_a), (x_b, y_b)]).length  # shapely
                        # print("length", length)
                        self.data_scale.clear()  # очищаем data_scale
                        self.result_lbl.setText(f"В отрезке {num_int} м: {round(length, 2)} пикселей")
                        self.scale_name.setText(f"{float(length) / num_int:.3f}")
                        self.draw_btn.setChecked(False)
                        self.del_all_item()

            elif self.type_act.currentIndex() == 2:
                self.del_all_item()  # удалим все Item
                if self.scale_name.text() == "":  # проверим есть ли масштаб
                    msg = QtWidgets.QMessageBox(self)
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Информация")
                    msg.setText("Не установлен масштаб")
                    msg.exec()
                    self.draw_btn.setChecked(False)
                    return
                if self.obj_coord.displayText() == "":
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                else:
                    self.data_point = json.loads(self.obj_coord.displayText())
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                self.draw_all_item(json.loads(self.obj_coord.displayText()))

                b = json.loads(self.obj_coord.displayText())
                if len(b) > 2:
                    i = 0
                    b_end = []
                    while i < len(b):
                        tuple_b = (float(b[i]), float(b[i + 1]))
                        b_end.append(tuple_b)
                        i += 2
                        if i == len(b):
                            break
                    length = LineString(b_end).length  # shapely
                    real_lenght = float(length) / float(self.scale_name.displayText())
                    real_lenght = round(real_lenght, 2)
                    self.result_lbl.setText(f'Длина линии {real_lenght}, м')

            elif self.type_act.currentIndex() == 3:
                self.del_all_item()  # удалим все Item
                if self.scale_name.text() == "":  # проверим есть ли масштаб
                    msg = QtWidgets.QMessageBox(self)
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Информация")
                    msg.setText("Не установлен масштаб")
                    self.draw_btn.setChecked(False)
                    msg.exec()
                    return
                if self.obj_coord.displayText() == "":
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                else:
                    self.data_point = json.loads(self.obj_coord.displayText())
                    self.data_point.append(str(event.scenePos().x()))  #
                    self.data_point.append(str(event.scenePos().y()))  # и запсываем в data_point
                    self.obj_coord.setText(json.dumps(self.data_point))
                    self.data_point.clear()
                self.draw_all_item(json.loads(self.obj_coord.displayText()))

                b = json.loads(self.obj_coord.displayText())
                if len(b) > 4:
                    i = 0
                    b_end = []
                    while i < len(b):
                        tuple_b = (float(b[i]), float(b[i + 1]))
                        b_end.append(tuple_b)
                        i += 2
                        if i == len(b):
                            break
                    area = Polygon(b_end).area  # shapely
                    real_area = float(area) / math.pow(float(self.scale_name.displayText()), 2)
                    real_area = round(real_area, 2)
                    self.result_lbl.setText(f'Площадь {real_area}, м2')

    def select_type_act(self):
        # При выборе нового действия нужно
        # снять с кнопки "Применить" нажатие
        # и удалить все item
        self.draw_btn.setChecked(False)
        self.del_all_item()
        # убрать все координаты
        self.obj_coord.setText("")

    def change_draw_btn(self):
        # при изменении нажатия кнопки
        # стереть все item
        self.del_all_item()
        # убрать все координаты
        self.obj_coord.setText("")

    def draw_all_item(self, coordinate):
        """
        Рисует все Item на картинке
        """
        if coordinate == []:
            return
        i = 0
        k = 0
        while i < len(coordinate):
            name_rings = MoveItem()
            name_rings.setPos(float(coordinate[i]), float(coordinate[i + 1]))
            self.scene.addItem(name_rings)
            i += 2
        while k < len(coordinate) - 2:
            line = QtWidgets.QGraphicsLineItem(float(coordinate[k]), float(coordinate[k + 1]),
                                               float(coordinate[k + 2]), float(coordinate[k + 3]))
            line.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
            self.scene.addItem(line)
            k -= 2
            k += 4

    def del_all_item(self):
        """
        Удаляет все Item с картинки
        """
        for item in self.scene.items():  # удалить все линии точки и линии
            str1 = str(item)
            str2 = 'QGraphicsLineItem'
            str3 = 'MoveItem'
            if str2 in str1:
                self.scene.removeItem(item)
            str1 = str(item)
            if str3 in str1:
                self.scene.removeItem(item)

    #     Функция выхода из программы
    def close_event(self) -> None:
        print("close")
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

    # 2. Вкладка ВИД
    # Функции инструментов ген.плана
    def scale_view_plus(self):  #
        """
        функция увеличения масштаба
        """
        self.scale += 0.05
        self.view.scale(self.scale, self.scale)
        self.scale = 1

    def scale_view_min(self):  #
        """
        функция уменьшения масштаба
        """
        self.scale -= 0.05
        self.view.scale(self.scale, self.scale)
        self.scale = 1

    def plan_hand(self):  # функция что бы появлялась рука для перетаскивания большой картинки
        """
        функция что бы появлялась рука для перетаскивания большой картинки
        """
        self.select_type_act()  # снять кнопку применить и координаты убрать
        if self.view.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        else:
            self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    # Функции инструментов ген.плана

    # 3. Вкладка СПРАВКА
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

    # ФУНКЦИИ ПРОГРАММЫ
    def select_color(self):
        # Определение цветов зон действия поражающих факторов
        get_color = QtWidgets.QColorDialog
        color = get_color.getColor(parent=self)
        color_rgb = color.getRgb()
        red = color_rgb[0]
        green = color_rgb[1]
        blue = color_rgb[2]
        # Какая кнопка послала сигнал?
        btn = self.sender()
        # Изменить цвет этой кнопке
        btn.setStyleSheet(f'background: rgb({red},{green},{blue});')
        # # RGB текущий цвет кнопки
        # btn_color = btn.palette().button().color()
        # print(btn_color.getRgb())

    def save_object(self):
        # проверка базы данных
        if self.is_there_a_database() == False:
            return
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        # Получить нужные переменные объекта
        scale = self.scale_name.text()
        obj_name = self.obj_name.text()
        obj_coord = self.obj_coord.text()
        obj_type = self.obj_type.currentIndex()
        check_list = [scale, obj_name, obj_coord, obj_type]
        # Проверка переменных на валидность
        if self.is_var_a_valid(check_list) == False:
            return
        get_state_obj = self.get_state_obj()  # получим состояние всех кнопок
        if get_state_obj == None:  # если мы в результате запроса self.get_state_obj()
            return  # получили None, то выйти из функции (введены не все данные)
        # проверяем есть ли уже такой ключ в словаре
        for key in self.data_obj.keys():
            if str(get_state_obj["obj_name"]) == key:  # если такой ключ уже есть
                dict_add = {str(get_state_obj["obj_name"]): get_state_obj}  # запишем все в глобальную переменную
                self.data_obj.update(dict_add)  # обновим словарь
                # вызов функции сохраннения словаря после того как ключ обновлен
                self.save_data_obj_vac()
                return  # и выйдем т.к. новый QStandardItem нет смысла делать

        #  если такого ключа нет, то добавим в словарь и создадим новый QStandardItem
        dict_add = {str(get_state_obj["obj_name"]): get_state_obj}  # запишем все в глобальную переменную
        self.data_obj.update(dict_add)
        # вызов функции сохраннения словаря после того как ключ добавлен
        self.save_data_obj_vac()
        # создадим новый QStandardItem на дереве
        key = QtGui.QStandardItem(str(get_state_obj["obj_name"]))
        self.all_items.setChild(self.all_items.rowCount(), key)

    def on_del_object(self, index):
        """
        Удаляет объект и удаляет его на дереве объектов
        """
        self.del_all_item()
        index = self.view_tree.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        if not item.parent() is None and item.parent().text().startswith('Объект'):
            if item.text().startswith('Объект'):
                return
            self.data_obj.pop(item.text(), None)  # по ключу мы удаляем объект из словаря data
            item.parent().removeRow(item.row())
        # вызов функции сохраннения словаря после того как ключ удален
        self.save_data_obj_vac()

    def save_data_obj_vac(self):
        """
        Обновляет словарь self.data_obj после изменения:
        - удаление объектов из дерева для стац.,лин. и объектов задний
        - добавление объектов на дерево для стац.,лин. и объектов задний
        """
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        data_in_base = cursorObj.fetchall()
        for row in data_in_base:
            if str(row[3]) + ',' + str(row[0]) == self.plan_list.currentText():
                cursorObj.execute('UPDATE objects SET data = ?  where id = ?', (str(self.data_obj), str(row[0])))
                sqliteConnection.commit()
        sqliteConnection.execute("VACUUM")
        cursorObj.close()

    def get_state_obj(self):
        """
        Функция фиксирует информацию  окон для записи
        и сохранения информации и возвращает словарь
        """
        data_obj = {}
        data_obj["obj_name"] = self.obj_name.text()
        data_obj["scale_name"] = self.scale_name.text()
        data_obj["obj_coord"] = self.obj_coord.text()
        data_obj["obj_type"] = self.obj_type.currentIndex()

        check_list = data_obj
        if "" in check_list.values():
            QtWidgets.QMessageBox.about(self, 'Ошибка', """Введены не все данные!""")
            return
        return data_obj

    def treefunction(self, index):
        """
        Фунция предназначена для работы с деревом объектов
        """
        # Удалить все линии и точки с карты
        self.del_all_item()
        # очистить поля
        self.zeroing_object()
        # Получить индекс с объекта
        ind = str(index.model().itemFromIndex(index).text())
        if ind == "Объекты:":  # если нажаты  объекты на дереве, то выход
            return
        # Если координаты по объекту есть, то нарисовать их на сцене
        if self.data_obj[ind].get('coord_app') == "":
            draw_point = {}
        else:
            draw_point = eval(self.data_obj[ind].get('obj_coord'))
        self.draw_all_item(draw_point)
        # установим значения для объекта
        self.obj_name.setText(self.data_obj[ind].get('obj_name'))
        self.scale_name.setText(self.data_obj[ind].get('scale_name'))
        self.obj_coord.setText(self.data_obj[ind].get('obj_coord'))
        self.obj_type.setCurrentIndex(self.data_obj[ind].get('obj_type'))

    def delete_end_point(self):
        "Удаление последней точки на объекте"
        if self.obj_coord.displayText() == "":
            return
        self.data_point = json.loads(self.obj_coord.displayText())  # преобразуем lineedit в список
        self.data_point.pop(-1)  # удалим последнюю точку (х,у)
        self.data_point.pop(-1)

        self.obj_coord.setText(json.dumps(self.data_point))  # запишем в lineedit список
        self.data_point.clear()  # очистим data_point
        self.del_all_item()  # очистим item
        self.draw_all_item(json.loads(self.obj_coord.displayText()))  # нарисуем все заново

    def delete_all_point(self):
        "Удаление всех координат"
        if self.obj_coord.displayText() == "":
            return
        self.obj_coord.setText("")
        self.del_all_item()

    # Рисование объектов
    def draw_all_object(self):
        # проверка базы данных
        if self.is_there_a_database() == False:
            return
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        # Проверка наличия объектов
        if self.any_objects_in_data_obj() == False:
            return
        # проверка равенства объектов Эксель и объектов карты
        if self.equality_obj() == False:
            return
        # определим все цвета зон
        color_zone_arr = self.get_color_for_zone()
        # достаем картинку из БД
        image_data = ''  # переменная хранения blob из базы данных
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        text = self.plan_list.currentText()
        for row in plant_in_db:
            if str(row[3]) + ',' + str(row[0]) == text:
                image_data = row[2]
        sqliteConnection.execute("VACUUM")
        cursorObj.close()

        if image_data == '':  # значит картинку не получили
            print("нет картинки")
            return
        if self.data_excel.text() == '':
            print("данных из экселя нет")
            return

        excel = eval(self.data_excel.text())
        # На основе исходной картинки создадим QImage и QPixmap
        qimg = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        pixmap_zone = QtGui.QPixmap(pixmap.width(), pixmap.height())
        pixmap_zone.fill(QtGui.QColor(0, 0, 0, 0))
        # Создадим QPainter
        qp = QtGui.QPainter(pixmap_zone)

        # Начнем рисование
        qp.begin(pixmap_zone)
        objects = self.data_obj.values()

        for zone_index in range(-1, -7, -1):
            i = 0
            for obj in objects:

                # возьмем масштаб оборудования
                scale_name = float(obj.get("scale_name"))
                # возьмем координаты оборудования
                obj_coord = eval(obj.get("obj_coord"))
                # возьмем тип объекта
                obj_type = obj.get("obj_type")
                # # начинаем рисовать с последнего цвета
                color = color_zone_arr[zone_index]
                zone = float(excel[i][zone_index]) * scale_name * 2  # т.к. на вход радиус, а нужен диаметр
                i += 1
                # зона может быть 0 тогда ничего рисовать не надо
                if zone == 0:
                    continue
                # определим ручку и кисточку
                pen = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2], color[3]), zone, QtCore.Qt.SolidLine)
                brush = QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2], color[3]))
                # со сглаживаниями
                pen.setJoinStyle(QtCore.Qt.RoundJoin)
                # закругленный концы
                pen.setCapStyle(QtCore.Qt.RoundCap)
                qp.setPen(pen)
                qp.setBrush(brush)

                if len(obj_coord) > 2:  # координаты можно преобразовать в полигон
                    if obj_type == 0:
                        # линейн. получим полигон
                        obj_coord = self.get_polygon(obj_coord)
                        qp.drawPolyline(obj_coord)
                    else:
                        # стац. об. получим полигон
                        obj_coord = self.get_polygon(obj_coord)
                        qp.drawPolyline(obj_coord)
                        qp.drawPolygon(obj_coord, QtCore.Qt.OddEvenFill)
                else:  # не получается полигон, значит точка
                    pen_point = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2], color[3]), 1, QtCore.Qt.SolidLine)
                    qp.setPen(pen_point)
                    point = QtCore.QPoint(int(float(obj_coord[0])), int(float(obj_coord[1])))
                    qp.drawEllipse(point, zone / 2, zone / 2)  # т.к. нужен радиус

        # Завершить рисование
        qp.end()
        # Положим одну картинку на другую
        painter = QtGui.QPainter(pixmap)
        painter.begin(pixmap)
        painter.setOpacity(self.opacity.value())
        painter.drawPixmap(0, 0, pixmap_zone)
        painter.end()
        # Разместим на сцене pixmap с pixmap_zone
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

    def draw_one_object(self):
        self.del_all_item()
        index = self.view_tree.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        if not item.parent() is None and item.parent().text().startswith('Объект'):
            if item.text().startswith('Объект'):
                return

        # проверка базы данных
        if self.is_there_a_database() == False:
            return
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        # Проверка наличия объектов
        if self.any_objects_in_data_obj() == False:
            return
        # определим все цвета зон
        color_zone_arr = self.get_color_for_zone()
        # достаем картинку из БД
        image_data = ''  # переменная хранения blob из базы данных
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        text = self.plan_list.currentText()
        for row in plant_in_db:
            if str(row[3]) + ',' + str(row[0]) == text:
                image_data = row[2]
        sqliteConnection.execute("VACUUM")
        cursorObj.close()

        if image_data == '':  # значит картинку не получили
            print("нет картинки")
            return
        if self.data_excel.text() == '':
            print("данных из экселя нет")
            return

        excel = eval(self.data_excel.text())
        # На основе исходной картинки создадим QImage и QPixmap
        qimg = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        pixmap_zone = QtGui.QPixmap(pixmap.width(), pixmap.height())
        pixmap_zone.fill(QtGui.QColor(0, 0, 0, 0))
        # Создадим QPainter
        qp = QtGui.QPainter(pixmap_zone)

        # Начнем рисование
        qp.begin(pixmap_zone)
        objects = self.data_obj.values()

        for zone_index in range(-1, -7, -1):
            i = 0
            for obj in objects:
                obj_name = obj.get("obj_name")
                if obj_name != item.text():
                    i += 1
                    continue
                else:
                    # возьмем масштаб оборудования
                    scale_name = float(obj.get("scale_name"))
                    # возьмем координаты оборудования
                    obj_coord = eval(obj.get("obj_coord"))
                    # возьмем тип объекта
                    obj_type = obj.get("obj_type")
                    # # начинаем рисовать с последнего цвета
                    color = color_zone_arr[zone_index]
                    zone = float(excel[i][zone_index]) * scale_name * 2  # т.к. на вход радиус, а нужен диаметр
                    i += 1
                    # зона может быть 0 тогда ничего рисовать не надо
                    if zone == 0:
                        continue
                    # определим ручку и кисточку
                    pen = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2], color[3]), zone, QtCore.Qt.SolidLine)
                    brush = QtGui.QBrush(QtGui.QColor(color[0], color[1], color[2], color[3]))
                    # со сглаживаниями
                    pen.setJoinStyle(QtCore.Qt.RoundJoin)
                    # закругленный концы
                    pen.setCapStyle(QtCore.Qt.RoundCap)
                    qp.setPen(pen)
                    qp.setBrush(brush)

                    if len(obj_coord) > 2:  # координаты можно преобразовать в полигон
                        if obj_type == 0:
                            # линейн. получим полигон
                            obj_coord = self.get_polygon(obj_coord)
                            qp.drawPolyline(obj_coord)
                        else:
                            # стац. об. получим полигон
                            obj_coord = self.get_polygon(obj_coord)
                            qp.drawPolyline(obj_coord)
                            qp.drawPolygon(obj_coord, QtCore.Qt.OddEvenFill)
                    else:  # не получается полигон, значит точка
                        pen_point = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2], color[3]), 1,
                                               QtCore.Qt.SolidLine)
                        qp.setPen(pen_point)
                        point = QtCore.QPoint(int(float(obj_coord[0])), int(float(obj_coord[1])))
                        qp.drawEllipse(point, zone / 2, zone / 2)  # т.к. нужен радиус

        #
        # Завершить рисование
        qp.end()
        # Положим одну картинку на другую
        painter = QtGui.QPainter(pixmap)
        painter.begin(pixmap)
        painter.setOpacity(self.opacity.value())
        painter.drawPixmap(0, 0, pixmap_zone)
        painter.end()
        # Разместим на сцене pixmap с pixmap_zone
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

    def draw_risk_object(self):
        print("Draw risk")
        # проверка базы данных
        if self.is_there_a_database() == False:
            return
        # Проверка ген.плана
        if self.is_there_a_plan() == False:
            return
        # Проверка наличия объектов
        if self.any_objects_in_data_obj() == False:
            return
        # проверка равенства объектов Эксель и объектов карты
        if self.equality_obj() == False:
            return
        # достаем картинку из БД
        image_data = ''  # переменная хранения blob из базы данных
        path_str = (f"{self.db_path.text()}/{self.db_name.text()}")
        path_str = path_str.replace("/", "//")
        sqliteConnection = sqlite3.connect(path_str)
        cursorObj = sqliteConnection.cursor()
        cursorObj.execute("SELECT * FROM objects")
        plant_in_db = cursorObj.fetchall()
        text = self.plan_list.currentText()
        for row in plant_in_db:
            if str(row[3]) + ',' + str(row[0]) == text:
                image_data = row[2]
        sqliteConnection.execute("VACUUM")
        cursorObj.close()

        if image_data == '':  # значит картинку не получили
            print("нет картинки")
            return
        if self.data_excel.text() == '':
            print("данных из экселя нет")
            return

        # На основе исходной картинки создадим QImage и QPixmap
        qimg = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        width, height = pixmap.width(), pixmap.height()
        # сделаем нулевую матрицу по размерам картинки
        zeors_array = np.zeros((width, height))

        excel = eval(self.data_excel.text())
        objects = self.data_obj.values()

        index = 0
        for obj in objects:
            # возьмем масштаб оборудования
            scale_name = float(obj.get("scale_name"))
            # возьмем координаты оборудования
            obj_coord = eval(obj.get("obj_coord"))
            # возьмем тип объекта
            obj_type = obj.get("obj_type")
            max_radius = excel[index][0] * scale_name
            power = self.power_data(max_radius)
            index += 1

            if len(obj_coord) > 2:  # координаты можно преобразовать в полигон или линию
                if obj_type == 0:
                    # линейн. получим полигон
                    obj_coord = self.get_polyline_shapely(obj_coord)
                    self.calc_el_zeors_array(width,height,obj_coord,power,zeors_array,scale_name)


                else:
                    # стац. об. получим полигон
                    obj_coord = self.get_polygon_shapely(obj_coord)
                    # print(obj_coord)
                    self.calc_el_zeors_array(width, height, obj_coord, power, zeors_array,scale_name)

            else:  # не получается полигон, значит точка
                obj_coord = Point(float(obj_coord[0]), float(obj_coord[1]))
                # print(obj_coord)
                self.calc_el_zeors_array(width, height, obj_coord, power, zeors_array,scale_name)

        plt.pcolormesh(zeors_array, cmap=plt.get_cmap('jet'), alpha=1)  # levels=levels сглаживание
        # plt.axis('off')
        plt.gca().invert_yaxis()
        plt.colorbar()
        plt.show()


    def get_color_for_zone(self) -> list:
        # по кнопкам определим зоны для рисования
        color_zone_arr = []
        color = self.color_zone1_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)
        color = self.color_zone2_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)
        color = self.color_zone3_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)
        color = self.color_zone4_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)
        color = self.color_zone5_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)
        color = self.color_zone6_btn.palette().button().color().getRgb()
        color_zone_arr.append(color)

        return color_zone_arr

    def get_data_excel(self):
        """
        Получение данных из файла excel.
        Количество столбцов не более 6, т.к. зон всего 6
        Количество строк равно равно количеству объектов
        """
        try:
            vals = Excel.Selection.Value
            if len(self.data_obj) != len(vals):
                print("строк больше чем объектов")
                self.data_excel.setText("")
            elif len(vals[0]) != 6:
                print("столбцов больше 6")
                self.data_excel.setText("")
            else:
                self.data_excel.setText(str(vals))
        except:
            print("Ошибка при считывании данных в экселе")
            self.data_excel.setText("")

    def get_polygon(self, coordinate):
        "На основе координат создает по QPoint QPolygon"
        i = 0
        points = []
        while i < len(coordinate):
            point = QtCore.QPoint(int(float(coordinate[i])), int(float(coordinate[i + 1])))
            points.append(point)
            i += 2
        polygon = QtGui.QPolygon(points)

        return polygon

    def get_polyline_shapely(self, coordinate):

        i = 0
        points = []
        while i < len(coordinate):
            point = (int(float(coordinate[i])), int(float(coordinate[i + 1])))
            points.append(point)
            i += 2
        polyline = LineString(points)

        return polyline

    def get_polygon_shapely(self, coordinate):

        i = 0
        points = []
        while i < len(coordinate):
            point = (int(float(coordinate[i])), int(float(coordinate[i + 1])))
            points.append(point)
            i += 2
        polygon = Polygon(points)

        return polygon

    def calc_el_zeors_array(self, width, height, object, power, zeors_array,scale_name):
        # power = [[power],[dist]]
        for x in range(width):
            for y in range(height):
                dist = round(Point(x, y).distance(object))*scale_name
                if dist == 0:
                    zeors_array[x, y] = zeors_array[x, y] + power[0][0]
                elif dist in power[1]:
                    find_index = power[1].index(dist)
                    zeors_array[x, y] = zeors_array[x, y] + power[0][find_index]
                else:
                    for i in power[1]:
                        if abs(dist-i)<0.001:
                            find_index = power[1].index(i)
                            zeors_array[x, y] = zeors_array[x, y] + power[0][find_index]
                            break

        return

    def power_data(self, max_r):

        radius = []
        power = [i / 100 for i in range(100)]

        for i in power:
            radius.append(max_r * i)
        power.sort(reverse=True)
        power_data = [power, radius]

        return power_data

    # Проверки программы
    def is_there_a_database(self) -> bool:
        if self.db_name.text() == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет подключенной базы данных")
            msg.exec()
            return False
        return True

    def is_there_a_plan(self) -> bool:
        if self.plan_list.currentText() == "--Нет ген.планов--":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Не выбран ген.план")
            msg.exec()
            return False
        return True

    def is_var_a_valid(self, check_list: list) -> bool:
        if "" in check_list:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Введены не все данные")
            msg.exec()
            return False
        return True

    def zeroing_object(self) -> None:
        """
        Функция обнуления объектов при переключении
        - планов
        - объектов
        - переход на корень дерева
        """
        self.obj_name.setText("")
        self.scale_name.setText("")
        self.obj_coord.setText("")
        self.obj_type.setCurrentIndex(0)

    def any_objects_in_data_obj(self):
        if self.data_obj == {}:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет объектов для рисования.")
            msg.exec()
            return False
        return True

    def equality_obj(self):
        if self.data_excel.text() == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Количество выделенных в Excel объектов не равно количеству объектов.")
            msg.exec()
            return False
        if len(eval(self.data_excel.text())) != len(self.data_obj):
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Количество выделенных в Excel объектов не равно количеству объектов.")
            msg.exec()
            return False
        return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    locale = 'ru_RU'
    qt_translator = QTranslator(app)
    qt_translator.load('{}/qtbase_{}.qm'.format(I18N_QT_PATH, locale))
    app_translator = QTranslator(app)
    app_translator.load('{}/{}.qm'.format(I18N_QT_PATH, locale))
    app.installTranslator(qt_translator)
    app.installTranslator(app_translator)
    ex = Painter()
    app.exec_()
