from PySide2 import QtWidgets, QtGui, QtCore
import os
import sys
from pathlib import Path
import random

sys.path.append(Path(os.getcwd()))
from class_db import Data_base



class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.db_name = ''
        self.db_path = ''

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Иконки
        path_ico = str(Path(os.getcwd()).parents[0])

        self.main_ico = QtGui.QIcon(path_ico + '/ico/comp.png')
        tree_ico = QtGui.QIcon(path_ico + '/ico/tree.png')

        paint_ico = QtGui.QIcon(path_ico + '/ico/painter.png')
        book_ico = QtGui.QIcon(path_ico + '/ico/book.png')
        word_ico = QtGui.QIcon(path_ico + '/ico/word.png')
        project_ico = QtGui.QIcon(path_ico + '/ico/project2.png')
        pen_ico = QtGui.QIcon(path_ico + '/ico/pen.png')
        download_ico = QtGui.QIcon(path_ico + '/ico/download.png')
        fire_ico = QtGui.QIcon(path_ico + '/ico/fire.png')
        explosion_ico = QtGui.QIcon(path_ico + '/ico/explosion.png')
        flash_ico = QtGui.QIcon(path_ico + '/ico/flash.png')
        show_ico = QtGui.QIcon(path_ico + '/ico/planshow.png')

        db_ico = QtGui.QIcon(path_ico + '/ico/data_base.png')
        ok_ico = QtGui.QIcon(path_ico + '/ico/ok.png')
        replace_ico = QtGui.QIcon(path_ico + '/ico/replace.png')
        save_ico = QtGui.QIcon(path_ico + '/ico/save.png')
        clear_ico = QtGui.QIcon(path_ico + '/ico/clear.png')
        del_ico = QtGui.QIcon(path_ico + '/ico/del.png')
        question_ico = QtGui.QIcon(path_ico + '/ico/question.png')
        scale_ico = QtGui.QIcon(path_ico + '/ico/scale.png')
        dist_ico = QtGui.QIcon(path_ico + '/ico/polyline.png')
        area_ico = QtGui.QIcon(path_ico + '/ico/area.png')
        object_ico = QtGui.QIcon(path_ico + '/ico/object.png')
        settings_ico = QtGui.QIcon(path_ico + '/ico/settings.png')
        draw_ico = QtGui.QIcon(path_ico + '/ico/draw.png')
        state_ico = QtGui.QIcon(path_ico + '/ico/state.png')
        tube_ico = QtGui.QIcon(path_ico + '/ico/tube.png')
        tree_ico = QtGui.QIcon(path_ico + '/ico/tree.png')
        exit_ico = QtGui.QIcon(path_ico + '/ico/exit.png')
        info_ico = QtGui.QIcon(path_ico + '/ico/info.png')
        color_ico = QtGui.QIcon(path_ico + '/ico/color_select.png')
        excel_ico = QtGui.QIcon(path_ico + '/ico/excel.png')
        plus_ico = QtGui.QIcon(path_ico + '/ico/plus.png')
        minus_ico = QtGui.QIcon(path_ico + '/ico/minus.png')
        dbl_minus_ico = QtGui.QIcon(path_ico + '/ico/double_minus.png')
        hand_ico = QtGui.QIcon(path_ico + '/ico/hand.png')
        risk_ico = QtGui.QIcon(path_ico + '/ico/risk.png')
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # Главное окно
        self.setGeometry(500, 500, 950, 750)
        self.setWindowTitle('Safety_risk')
        self.setWindowIcon(self.main_ico)
        # Центральный виджет
        central_widget = QtWidgets.QWidget()
        central_grid = QtWidgets.QGridLayout(self)
        central_grid.setColumnStretch(0, 1)
        central_grid.setColumnStretch(1, 7)
        central_grid.setRowStretch(0, 7)
        central_grid.setRowStretch(1, 1)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 1. Генплан
        # Рамка
        layout_picture = QtWidgets.QFormLayout(self)
        GB_picture = QtWidgets.QGroupBox('План расположения')
        GB_picture.setStyleSheet("QGroupBox { font-weight : bold; }")
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
        layout_picture.addRow("", self.area)
        GB_picture.setLayout(layout_picture)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 2. Панель набора действий
        # т.к. данных  много создадим вкладки табов
        tabs = QtWidgets.QTabWidget()  # создаем набор вкладок табов
        # 2.1 Главная вкладка (масштаб, измерения, выбор генплана, состояние подключения к БД)
        tab_main = QtWidgets.QWidget()
        # 2.2. Зоны поражения
        tab_draw = QtWidgets.QWidget()
        # 2.3. Ситуационные планы
        tab_report = QtWidgets.QWidget()
        # добавляем к п.2.1. на главную вкладку
        tabs.addTab(tab_main, "")
        tabs.setTabIcon(0, project_ico)
        tabs.setTabToolTip(0, "Основные действия")
        tab_main.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.2. на вкладку зон поражения
        tabs.addTab(tab_draw, "")  # 2. Зоны поражения
        tabs.setTabIcon(1, paint_ico)
        tabs.setTabToolTip(1, "Зоны поражения")
        tab_draw.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.3. на вкладку ситуационных планов
        tabs.addTab(tab_report, "")  # 3. Ситуационные планы
        tabs.setTabIcon(2, word_ico)
        tabs.setTabToolTip(2, "Отчет")
        tab_report.layout = QtWidgets.QFormLayout(self)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 2.1.1. Рамка №1. Главной вкладки. Маштаб  (то что будет в рамке 1)
        self.scale_plan = QtWidgets.QLineEdit()
        self.scale_plan.setPlaceholderText("Масштаб")
        self.scale_plan.setToolTip("В одном пикселе метров")
        self.scale_plan.setReadOnly(True)
        # Упаковываем все в QGroupBox
        # Рамка №1
        layout_scale = QtWidgets.QFormLayout(self)
        GB_scale = QtWidgets.QGroupBox('Масштаб')
        GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_scale.addRow("", self.scale_plan)
        GB_scale.setLayout(layout_scale)

        # 2.1.2. Рамка №2. Главной вкладки. Действия (масштаб, расстояние, площадь)  (то что будет в рамке 2)
        self.type_act = QtWidgets.QComboBox() # тип действия
        self.type_act.addItems(["Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, scale_ico)
        self.type_act.setItemIcon(1, dist_ico)
        self.type_act.setItemIcon(2, area_ico)
        # self.type_act.activated[str].connect(self.select_type_act)
        self.result_type_act = QtWidgets.QLabel() # для вывода результата применения type_act + draw_type_act
        self.draw_type_act = QtWidgets.QPushButton("Применить")
        # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        self.draw_type_act.setCheckable(True)
        self.draw_type_act.setChecked(False)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_act = QtWidgets.QFormLayout(self)
        GB_act = QtWidgets.QGroupBox('Действие')
        GB_act.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_act.addRow("", self.type_act)
        layout_act.addRow("", self.draw_type_act)
        layout_act.addRow("", self.result_type_act)
        GB_act.setLayout(layout_act)

        # 2.1.3. Рамка №3. Главной вкладки. Ситуацилнные планы. (то что будет в рамке 3)
        self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
        self.plan_list.addItems(["--Нет ген.планов--"])
        self.plan_list.setToolTip("""Ген.планы объекта""")
        # # self.plan_list.activated[str].connect(self.plan_list_select)
        self.data_base_info_connect = QtWidgets.QLabel()  # информация о подключении базы данных
        self.data_base_info_connect.setText('Нет подключения к базе данных...')
        self.data_base_info_connect.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.data_base_info_connect.setStyleSheet('color: red')


        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_plan = QtWidgets.QFormLayout(self)
        GB_plan = QtWidgets.QGroupBox('Выбор ген.плана')
        GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_plan.addRow("", self.plan_list)
        layout_plan.addRow("", self.data_base_info_connect)
        GB_plan.setLayout(layout_plan)

        # Собираем рамки №№ 1-3
        tab_main.layout.addWidget(GB_scale)
        tab_main.layout.addWidget(GB_act)
        tab_main.layout.addWidget(GB_plan)
        # Размещаем на табе рамки №№ 1-2
        tab_main.setLayout(tab_main.layout)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 2.2.1. Рамка №1. Владки зон поражения. (то что будет в рамке 1)
        # color_zone набор кнопок для зон 6 возможных зон поражения
        self.color_zone1_btn = QtWidgets.QPushButton("Зона 1")
        self.color_zone1_btn.setIcon(color_ico)
        self.color_zone1_btn.setToolTip("Цвет зоны 1")
        self.color_zone1_btn.setStyleSheet("background-color: red")
        # self.color_zone1_btn.clicked.connect(self.select_color)
        self.color_zone2_btn = QtWidgets.QPushButton("Зона 2")
        self.color_zone2_btn.setIcon(color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.color_zone2_btn.clicked.connect(self.select_color)
        self.color_zone3_btn = QtWidgets.QPushButton("Зона 3")
        self.color_zone3_btn.setIcon(color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.color_zone3_btn.clicked.connect(self.select_color)
        self.color_zone4_btn = QtWidgets.QPushButton("Зона 4")
        self.color_zone4_btn.setIcon(color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.color_zone4_btn.clicked.connect(self.select_color)
        self.color_zone5_btn = QtWidgets.QPushButton("Зона 5")
        self.color_zone5_btn.setIcon(color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.color_zone5_btn.clicked.connect(self.select_color)
        self.color_zone6_btn = QtWidgets.QPushButton("Зона 6")
        self.color_zone6_btn.setIcon(color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.color_zone6_btn.clicked.connect(self.select_color)

        # 2.2.2. Рамка №2. Владки зон поражения. (то что будет в рамке 2)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)
        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        # self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        # self.get_data_btn.clicked.connect(self.get_data_excel)

        # 2.2.3. Рамка №3. Владки зон поражения. (то что будет в рамке 3)
        self.opacity = QtWidgets.QDoubleSpinBox()
        self.opacity.setDecimals(1)
        self.opacity.setRange(0, 1)
        self.opacity.setSingleStep(0.1)
        self.opacity.setValue(0.5)

        # Упаковываем все на вкладку таба "1" (делаем все в QGroupBox)
        # Рамка №1
        layout_zone = QtWidgets.QFormLayout(self)
        GB_zone = QtWidgets.QGroupBox('Выбор цвета')
        GB_zone.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_zone_1_2 = QtWidgets.QHBoxLayout()
        hbox_zone_1_2.addWidget(self.color_zone1_btn)
        hbox_zone_1_2.addWidget(self.color_zone2_btn)
        layout_zone.addRow("", hbox_zone_1_2)
        hbox_zone_3_4 = QtWidgets.QHBoxLayout()
        hbox_zone_3_4.addWidget(self.color_zone3_btn)
        hbox_zone_3_4.addWidget(self.color_zone4_btn)
        layout_zone.addRow("", hbox_zone_3_4)
        hbox_zone_5_6 = QtWidgets.QHBoxLayout()
        hbox_zone_5_6.addWidget(self.color_zone5_btn)
        hbox_zone_5_6.addWidget(self.color_zone6_btn)
        layout_zone.addRow("", hbox_zone_5_6)
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

        # Собираем рамки №№ 1-3
        tab_draw.layout.addWidget(GB_zone)
        tab_draw.layout.addWidget(GB_xl)
        tab_draw.layout.addWidget(GB_opacity)
        # Размещаем на табе
        tab_draw.setLayout(tab_draw.layout)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 2.3.1. Рамка №1. Вкладка отчетов. Организация  (то что будет в рамке 1)
        self.organization = QtWidgets.QComboBox() # тип организации
        self.organization.addItems(["--Выбрать организацию--"])
        # # self.type_act.activated[str].connect(self.select_type_act)
        self.organization_add = QtWidgets.QPushButton("Добавить")
        self.organization_add.setIcon(plus_ico)
        # # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        self.organization_edit = QtWidgets.QPushButton("Редактировать")
        self.organization_edit.setIcon(pen_ico)
        # # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        self.organization_del = QtWidgets.QPushButton("Удалить")
        self.organization_del.setIcon(minus_ico)
        # # self.draw_type_act.clicked.connect(self.change_draw_type_act)
        #
        # # Упаковываем все в QGroupBox
        # # Рамка №1
        layout_org = QtWidgets.QFormLayout(self)
        GB_org = QtWidgets.QGroupBox('Организация')
        GB_org.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_org.addRow("", self.organization)
        hbox_org = QtWidgets.QHBoxLayout()
        hbox_org.addWidget(self.organization_add)
        hbox_org.addWidget(self.organization_edit)
        hbox_org.addWidget(self.organization_del)
        layout_org.addRow("", hbox_org)
        GB_org.setLayout(layout_org)

        # 2.3.2. Рамка №2. Вкладка отчетов. Тип документа  (то что будет в рамке 2)
        self.type_doc = QtWidgets.QComboBox() # тип документа
        self.type_doc.addItems(["ДПБ", "ПМ ГОЧС"])
        self.type_doc.setItemIcon(0, word_ico)
        self.type_doc.setItemIcon(1, word_ico)
        # # self.type_act.activated[str].connect(self.select_type_act)
        doc_report = QtWidgets.QPushButton("Сохранить")
        doc_report.setIcon(download_ico)
        # # self.draw_type_act.clicked.connect(self.change_draw_type_act)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_doc = QtWidgets.QFormLayout(self)
        GB_doc = QtWidgets.QGroupBox('Выбор документа')
        GB_doc.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_doc = QtWidgets.QHBoxLayout()
        hbox_doc.addWidget(self.type_doc)
        hbox_doc.addWidget(doc_report)
        layout_doc.addRow("", hbox_doc)
        GB_doc.setLayout(layout_doc)

        # 2.3.3. Рамка №3. Вкладка отчетов. Тип плана  (то что будет в рамке 3)
        self.type_plan = QtWidgets.QComboBox() # тип плана
        self.type_plan.addItems(["Взрыв", "Пожар", "Вспышка", "Риск"])
        self.type_plan.setItemIcon(0, explosion_ico)
        self.type_plan.setItemIcon(1, fire_ico)
        self.type_plan.setItemIcon(2, flash_ico)
        self.type_plan.setItemIcon(3, risk_ico)
        # # self.type_act.activated[str].connect(self.select_type_act)
        plan_report = QtWidgets.QPushButton("Нарисовать")
        plan_report.setIcon(show_ico)
        # # self.draw_type_act.clicked.connect(self.change_draw_type_act)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_get_plan = QtWidgets.QFormLayout(self)
        GB_get_plan = QtWidgets.QGroupBox('Ситуационный план')
        GB_get_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_get_plan = QtWidgets.QHBoxLayout()
        hbox_get_plan.addWidget(self.type_plan)
        hbox_get_plan.addWidget(plan_report)
        layout_get_plan.addRow("", hbox_get_plan)
        GB_get_plan.setLayout(layout_get_plan)


        # Собираем рамки №№ 1-3
        tab_report.layout.addWidget(GB_org)
        tab_report.layout.addWidget(GB_doc)
        tab_report.layout.addWidget(GB_get_plan)
        # Размещаем на табе рамки №№ 1-2
        tab_report.setLayout(tab_report.layout)
        # # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # 3. Таблица для ввода данных

        # Рамка
        layout_data = QtWidgets.QFormLayout(self)
        GB_data = QtWidgets.QGroupBox('Данные об объекте')
        GB_data.setStyleSheet("QGroupBox { font-weight : bold; }")

        # таблица
        data_grid = QtWidgets.QGridLayout(self)
        data_grid.setColumnStretch(0, 15)
        data_grid.setColumnStretch(1, 1)

        self.table_data = QtWidgets.QTableWidget(0, 32)
        self.table_data_view()  # фукция отрисовки заголовков таблицы
        # кнопки управления
        layout_control = QtWidgets.QFormLayout(self)
        GB_control = QtWidgets.QGroupBox('Действия объекта')

        self.add_row = QtWidgets.QPushButton("Добавить объект")
        self.add_row.setStyleSheet("text-align: left;")
        self.add_row.setIcon(plus_ico)
        self.add_row.setToolTip("Добавить строку в таблицу")
        self.add_row.clicked.connect(self.add_in_table)

        self.del_row = QtWidgets.QPushButton("Удалить объект")
        self.del_row.setStyleSheet("text-align: left;")
        self.del_row.setIcon(minus_ico)
        self.del_row.setToolTip("Удалить строку из таблицу")
        self.del_row.clicked.connect(self.del_in_table)

        self.example_obj = QtWidgets.QPushButton("Пример объекта")
        self.example_obj.setStyleSheet("text-align: left;")
        self.example_obj.setIcon(book_ico)
        self.example_obj.setToolTip("Добавить примерный объект")
        self.example_obj.clicked.connect(self.add_example_obj)

        self.draw_obj = QtWidgets.QPushButton("Координаты")
        self.draw_obj.setStyleSheet ("text-align: left;")
        self.draw_obj.setToolTip('Указать координаты выбранного в таблице объекта')
        self.draw_obj.setIcon(object_ico)
        # self.draw_obj.clicked.connect(self.change_draw_type_act)
        self.draw_obj.setCheckable(True)
        self.draw_obj.setChecked(False)

        layout_control.addRow("", self.add_row)
        layout_control.addRow("", self.del_row)
        layout_control.addRow("", self.example_obj)
        layout_control.addRow("", self.draw_obj)
        GB_control.setLayout(layout_control)

        data_grid.addWidget(self.table_data, 0, 0, 1, 1)
        data_grid.addWidget(GB_control, 0, 1, 1, 1)
        layout_data.addRow("", data_grid)
        GB_data.setLayout(layout_data)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # 4. Размещение основных элементов на центральной сетке
        central_grid.addWidget(GB_picture, 0, 0, 1, 0)
        central_grid.addWidget(tabs, 1, 0, 1, 1)
        central_grid.addWidget(GB_data, 1, 1, 1, 1)
        central_widget.setLayout(central_grid)
        self.setCentralWidget(central_widget)
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # 5. Меню (тулбар)
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
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if not parent:
            self.show()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Группа функций работы с таблицей self.table_data
    def table_data_view(self):
        """
        Оформление таблицы для введения данных self.table_data
        """

        header_list = ['Позиция', 'Наименование', 'Локация',
                       'Материал', 'Расположение',
                       'Назначение']

        for header in header_list:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(225, 225, 225))
            self.table_data.setHorizontalHeaderItem(header_list.index(header), item)

        header_list_tech = ['Длина, км', 'Диаметр, мм', 'Давление, кПа',
                            'Тем-ра, гр.С', 'Объем, м3',
                            'Ст.заполн., -', 'Обвалование, м2', 'Тип']

        for header in header_list_tech:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(200, 255, 200))
            poz = header_list_tech.index(header) + len(header_list)
            if header == 'Тип':
                item.setToolTip(
                    '''
                    Тип оборудования:

                    0 - трубопровод
                    1 - емкость под давлением
                    2 - насос герметичный
                    3 - колонны конденсаторы фильтры
                    4 - резервуар хранения
                    5 - теплообменники
                    6 - цистерны
                    '''
                )

            self.table_data.setHorizontalHeaderItem(poz, item)

        header_list_sub = ['fp, 1/м', 'z, -', 'po ж.ф., кг/м3',
                           'po г.ф., кг/м3', 'М, кг/кмоль', 'Pn, кПа',
                           'Твсп, гр.С', 'Ткип, гр.С', 'Класс в-ва', 'Вид пространства',
                           'Qсг, кДж/кг', 'sigma, -', 'Энергозапас, -', 'S, млн.руб/т']

        for header in header_list_sub:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(200, 255, 255))
            poz = header_list_sub.index(header) + len(header_list) + len(header_list_tech)

            self.table_data.setHorizontalHeaderItem(poz, item)

            if header == 'fp, 1/м':
                item.setToolTip(
                    """
                    Коэф. толщины слоя:

                    5  -  при проливе на неспланированную грунтовую поверхность;
                    20 -  при проливе на спланированное грунтовое покрытие;
                    150 - при проливе на бетонное или асфальтовое покрытие.
                    """
                )
            elif header == 'z, -':
                item.setToolTip(
                    """
                    Коэф. участия во взрыве:

                    0,1  -  на открытой площадке
                    """
                )
            elif header == 'po ж.ф., кг/м3' or header == 'po г.ф., кг/м3':
                item.setToolTip('Плотность жидкой или газовой фазы')
            elif header == 'М, кг/кмоль':
                item.setToolTip('Молярная масса')
            elif header == 'Pn, кПа':
                item.setToolTip('Давление насыщенного пара')
            elif header == 'Твсп, гр.С':
                item.setToolTip('Температура вспышки')
            elif header == 'Ткип, гр.С':
                item.setToolTip('Температура кипения')
            elif header == 'Класс в-ва':
                item.setToolTip(
                    """
                    Классификация горючих веществ по степени чувствительности:

                    Класс 1 - Особо чувствительные вещества;
                    Класс 2 - Чувствительные вещества;
                    Класс 3 - Средне-чувствительные вещества;
                    Класс 4 - Слабочувствительные вещества.
                    """
                )
            elif header == 'Вид пространства':
                item.setToolTip(
                    """
                    Классификация горючих веществ по степени чувствительности:

                    Вид 1. Наличие длинных труб, полостей, каверн, заполненных горючей смесью;
                    Вид 2. Сильно загроможденное пространство: наличие полузамкнутых объемов,
                    высокая плотность оборудования;

                    Вид 3. Средне загроможденное пространство: отдельно стоящие технологические установки;
                    Вид 4. Слабо загроможденное и свободное пространство.
                    """
                )
            elif header == 'Qсг, кДж/кг':
                item.setToolTip('Теплота сгорания')
            elif header == 'sigma, -':
                item.setToolTip("""
                Параметр горения:
                sigma = 7 (пар и/или газ)
                sigma = 4 (газокапельная смесь)
                """)
            elif header == 'Энергозапас, -':
                item.setToolTip('1 - легкий газ; 2 - тяжелый газ')
            elif header == 'S, млн.руб/т':
                item.setToolTip('Стоимость вещества')

        header_list_obj = ['Погиб., чел', 'Постр., чел', 'Пребывание, -',
                           'Координаты']

        for header in header_list_obj:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(255, 200, 200))
            poz = header_list_obj.index(header) + len(header_list) + \
                  len(header_list_tech) + len(header_list_sub)
            self.table_data.setHorizontalHeaderItem(poz, item)
            if header == 'Пребывание, -':
                item.setToolTip('Вероятность пребывания: 8 часов / 24 часа = 0,33')

    def add_in_table(self):
        count_row = self.table_data.rowCount()  # посчитаем количество строк
        self.table_data.insertRow(count_row)

    def del_in_table(self):
        index = self.table_data.currentIndex()
        self.table_data.removeRow(index.row())

    def add_example_obj(self):

        data_list = [
            [f'Е-{random.randint(1,20)}', 'Емкость', 'Наземная', 'Сталь', 'ДНС-2', 'Хранение нефти',
             '0', '0', '0,8', '10', f'{random.randrange(100, 500, 100)}', '0.8 ', f'{random.randrange(100, 500, 25)}', '1', ],
            ['Нефтепровод от т.10 до УПСВ', 'Нефтепровод', 'Поздемная', 'Сталь В20', 'Ивинское м.н.', 'Транспорт нефти',
             '0,985', f'{random.choice([89,114,159,219])}', '1.25', '10', '0', '0 ', '0', '0', ]
        ]
        # Добавить данные
        count_row = self.table_data.rowCount()  # посчитаем количество строк

        for item in data_list:  # возьмем каждый словарь из data_list
            count_col = 0  # колонка с индесом 0
            # вставим строку, т.е. если строк 0, то на 0 позицию по индексу,
            # если кол-во строк 1 то на 1 позицию по индексу
            self.table_data.insertRow(count_row)
            for var in item:  # для каждого значения из словаря item пробежим по столбцам
                TableWidgetItem = QtWidgets.QTableWidgetItem(var)
                self.table_data.setItem(count_row, count_col, TableWidgetItem)
                count_col += 1  # + 1 к столбцу
            count_row += 1  # +1 к строке (новая строка если len(data_list) > 1)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Группа функций для работы с азой данных
    def db_create(self):
        self.db_name, self.db_path = Data_base(self.db_name, self.db_path).db_create()
        self.connect_info(self.db_name, self.db_path)

    def db_connect(self):
        self.db_name, self.db_path = Data_base(self.db_name, self.db_path).db_connect()
        self.connect_info(self.db_name, self.db_path)
    #     TODO Поставить функцию очиски ген.плана

    def connect_info(self, name:str, path:str):
        """
        Проверка наличия данных о подключения БД
        Путь и имя базы данных не равны пустым строкам
        """
        if path != '' and name != '':
            self.data_base_info_connect.setText(f'База  данных {self.db_name} подключена!')
            self.data_base_info_connect.setStyleSheet('color: green')
        else:
            self.data_base_info_connect.setText('Нет подключения к базе данных...')
            self.data_base_info_connect.setStyleSheet('color: red')

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    ex = Painter()
    app.exec_()
