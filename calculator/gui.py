import math
import time

from PySide2 import QtWidgets, QtGui, QtCore, QtSql
import os
import sys
from pathlib import Path
import random

from shapely.geometry import LineString, Polygon
import xlwings as xw
import numpy as np
# db
from data_base import class_db
# data
from draw_for_calculator import class_data_draw
from report_for_calculator import class_opo

I18N_QT_PATH = str(os.path.join(os.path.abspath('.'), 'i18n'))
TIME_EVAPORATED = 3600
MASS_BURNOUT_RATE = 0.06
WIND_VELOCITY = 1
PATH_LOCAL_BASE = Path.cwd()
LOCAL_BASE = QtSql.QSqlDatabase("QSQLITE")
LOCAL_BASE.setDatabaseName("local_base.db")
LOCAL_BASE.open()
FRACTIONS_OIL = (20, 34, 2, 3, 4, 220, 32)


class Edit_table_org(QtWidgets.QWidget):
    """
    Форма редактирования таблицы с организациями
    из базы данных local_base.db
    """

    def __init__(self):
        super().__init__()
        path_ico = str(Path(os.getcwd()).parents[0])
        self.main_ico = QtGui.QIcon(path_ico + '/ico/comp.png')
        self.setWindowTitle('База данных организаций')
        self.setWindowIcon(self.main_ico)

        layout = QtWidgets.QVBoxLayout()
        self.table = QtWidgets.QTableView()
        self.model = QtSql.QSqlTableModel(db=LOCAL_BASE)
        self.table.setModel(self.model)
        self.model.setTable("organization")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Наим.полн.")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Руководитель")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Ф.И.О.")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Техн.рук-ль")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, "Ф.И.О.")
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, "Адрес полн.")
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, "Адрес сокр.")
        self.model.setHeaderData(9, QtCore.Qt.Horizontal, "Месторождение")
        self.model.setHeaderData(10, QtCore.Qt.Horizontal, "Юр.адрес")
        self.model.setHeaderData(11, QtCore.Qt.Horizontal, "Тел.")
        self.model.setHeaderData(12, QtCore.Qt.Horizontal, "Почта")
        self.model.setHeaderData(13, QtCore.Qt.Horizontal, "Объект")
        self.model.setHeaderData(14, QtCore.Qt.Horizontal, "Ср.смена")
        self.model.setHeaderData(15, QtCore.Qt.Horizontal, "Макс.смена")
        self.model.setHeaderData(16, QtCore.Qt.Horizontal, "Лицензия")
        self.model.setHeaderData(17, QtCore.Qt.Horizontal, "Дата выдачи")
        self.model.setHeaderData(18, QtCore.Qt.Horizontal, "ОТ и ПБ")

        self.model.select()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.showMaximized()


class Object_point(QtWidgets.QGraphicsItem):
    def __init__(self, thickness):
        super().__init__()
        self.tag = None
        self.thickness = thickness

    def boundingRect(self):
        # print('boundingRect')
        return QtCore.QRectF(-(self.thickness), -(self.thickness), self.thickness, self.thickness)

    def paint(self, painter, option, widget):  # рисуем новый квадрат со стороной 10
        # print('paint')
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QtCore.Qt.red)
        painter.drawRect(-(self.thickness), -(self.thickness), self.thickness, self.thickness)


class Painter(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # Иконки
        path_ico = str(Path(os.getcwd()).parents[0])

        self.main_ico = QtGui.QIcon(path_ico + '/ico/comp.png')

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
        cloud_ico = QtGui.QIcon(path_ico + '/ico/cloud.png')

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
        # Глобальные переменные в программе
        # а) Список для запоминания координат для определения масштаба
        # по следующему алгоритму:
        # при каждом нажатии на ген.план запоминает координаты клика (х,у)
        # затем при len(self.data_draw_point) == 4, запрашивает у пользователя
        # QInputDialog число, чему этом отрезок равен в метрах и вычисляется масштаб
        # self.data_draw_point становится [].

        self.data_draw_point = []

        # б. Переменная отвечающая за индекс строки в self.table_data
        self.row_ind_in_data_grid = None

        # в. Переменные отвечающие за подключение БД
        self.db_name = ''
        self.db_path = ''

        # г. Переменная ген.плана
        self.scale = 1

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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
        self.scene.mousePressEvent = self.scene_press_event
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
        # 2.4. Настройки
        tab_settings = QtWidgets.QWidget()
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
        tabs.addTab(tab_report, "")  # 3. Отчет
        tabs.setTabIcon(2, word_ico)
        tabs.setTabToolTip(2, "Отчет")
        tab_report.layout = QtWidgets.QFormLayout(self)
        # добавляем к п.2.4. на вкладку ситуационных планов
        tabs.addTab(tab_settings, "")  # 3. Ситуационные планы
        tabs.setTabIcon(3, settings_ico)
        tabs.setTabToolTip(3, "Настройки")
        tab_settings.layout = QtWidgets.QFormLayout(self)
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
        self.type_act = QtWidgets.QComboBox()  # тип действия
        self.type_act.addItems(["Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, scale_ico)
        self.type_act.setItemIcon(1, dist_ico)
        self.type_act.setItemIcon(2, area_ico)
        self.type_act.activated[str].connect(self.select_type_act)
        self.result_type_act = QtWidgets.QLabel()  # для вывода результата применения type_act + draw_type_act
        self.draw_type_act = QtWidgets.QPushButton("Применить")
        self.draw_type_act.clicked.connect(self.change_draw_type_act)
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
        self.plan_list.activated[str].connect(self.plan_list_select)
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

        # 2.2.2. Рамка №2. Владки зон поражения. (то что будет в рамке 2)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)

        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        self.get_data_btn.clicked.connect(self.get_data_excel)

        self.draw_from_excel = QtWidgets.QPushButton("Рисовать")
        self.draw_from_excel.setIcon(paint_ico)
        self.draw_from_excel.setToolTip("Отрисовка зон из Excel")
        self.draw_from_excel.clicked.connect(lambda: self.draw_from_data([] if self.data_excel.text() == ''
                                                                         else eval(self.data_excel.text())))

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
        hbox_xl_draw = QtWidgets.QHBoxLayout()
        hbox_xl_draw.addWidget(self.get_data_btn)
        hbox_xl_draw.addWidget(self.draw_from_excel)
        layout_xl.addRow("", hbox_xl_draw)
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
        self.organization = QtWidgets.QComboBox()  # тип организации
        self.organization.addItems(class_db.Data_base('local_base.db', str(PATH_LOCAL_BASE)).get_organizations())
        # # self.type_act.activated[str].connect(self.select_type_act)
        self.organization_edit = QtWidgets.QPushButton("Редактировать")
        self.organization_edit.setIcon(pen_ico)
        self.organization_edit.clicked.connect(self.edit_organization)
        self.organization_del = QtWidgets.QPushButton("Удалить")
        self.organization_del.setIcon(minus_ico)
        self.organization_del.clicked.connect(self.delete_organization)

        # # Упаковываем все в QGroupBox
        # # Рамка №1
        layout_org = QtWidgets.QFormLayout(self)
        GB_org = QtWidgets.QGroupBox('Организация')
        GB_org.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_org.addRow("", self.organization)
        hbox_org = QtWidgets.QHBoxLayout()
        hbox_org.addWidget(self.organization_edit)
        hbox_org.addWidget(self.organization_del)
        layout_org.addRow("", hbox_org)
        GB_org.setLayout(layout_org)

        # 2.3.2. Рамка №2. Вкладка отчетов. Тип документа  (то что будет в рамке 2)
        self.type_doc = QtWidgets.QComboBox()  # тип документа
        self.type_doc.addItems(["ДПБ", "ПМ ГОЧС"])
        self.type_doc.setItemIcon(0, word_ico)
        self.type_doc.setItemIcon(1, word_ico)
        self.doc_report = QtWidgets.QPushButton("Сохранить")
        self.doc_report.setIcon(download_ico)
        self.doc_report.clicked.connect(self.report_word)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_doc = QtWidgets.QFormLayout(self)
        GB_doc = QtWidgets.QGroupBox('Выбор документа')
        GB_doc.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_doc = QtWidgets.QHBoxLayout()
        hbox_doc.addWidget(self.type_doc)
        hbox_doc.addWidget(self.doc_report)
        layout_doc.addRow("", hbox_doc)
        GB_doc.setLayout(layout_doc)

        # 2.3.3. Рамка №3. Вкладка отчетов. Тип плана  (то что будет в рамке 3)
        self.plan_report_type = QtWidgets.QComboBox()  # тип плана
        self.plan_report_type.addItems(["Взрыв", "Пожар", "Вспышка", "НКПР", "Риск"])
        self.plan_report_type.setItemIcon(0, explosion_ico)
        self.plan_report_type.setItemIcon(1, fire_ico)
        self.plan_report_type.setItemIcon(2, flash_ico)
        self.plan_report_type.setItemIcon(3, cloud_ico)
        self.plan_report_type.setItemIcon(4, risk_ico)
        # # self.type_act.activated[str].connect(self.select_type_act)
        self.plan_report = QtWidgets.QPushButton("Нарисовать")
        self.plan_report.setIcon(show_ico)
        self.plan_report.clicked.connect(self.plan_report_draw)

        # Упаковываем все в QGroupBox
        # Рамка №2
        layout_get_plan = QtWidgets.QFormLayout(self)
        GB_get_plan = QtWidgets.QGroupBox('Ситуационный план')
        GB_get_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_get_plan = QtWidgets.QHBoxLayout()
        hbox_get_plan.addWidget(self.plan_report_type)
        hbox_get_plan.addWidget(self.plan_report)
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
        # 2.4.1. Рамка №1. Толщина линий объектов   (то что будет в рамке 1)
        self.thickness_line = QtWidgets.QSpinBox()
        self.thickness_line.setRange(1, 10)
        self.thickness_line.setSingleStep(1)
        self.thickness_line.setValue(2)
        self.thickness_line.setToolTip("Толщина линий объектов")

        self.fill_thickness = QtWidgets.QSpinBox()
        self.fill_thickness.setRange(0, 30)
        self.fill_thickness.setSingleStep(1)
        self.fill_thickness.setValue(10)
        self.fill_thickness.setToolTip("Толщина изолиний зон поражающего фактора")

        # 2.4.2. Рамка №2. Подробность расчета риска   (то что будет в рамке 2)
        self.sharpness = QtWidgets.QSpinBox()
        self.sharpness.setRange(1, 10)
        self.sharpness.setSingleStep(1)
        self.sharpness.setValue(5)

        # 2.4.3. Рамка №3. Время истечения   (то что будет в рамке 3)
        self.shutdown_time = QtWidgets.QSpinBox()
        self.shutdown_time.setToolTip("Время отключения трубопроводов в секундах")
        self.shutdown_time.setRange(0, 600)
        self.shutdown_time.setSingleStep(1)
        self.shutdown_time.setValue(0)

        #
        # # Упаковываем все в QGroupBox
        # # Рамка №1
        layout_set = QtWidgets.QFormLayout(self)
        GB_set = QtWidgets.QGroupBox('Толщина линий')
        GB_set.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_fill = QtWidgets.QHBoxLayout()
        hbox_fill.addWidget(self.thickness_line)
        hbox_fill.addWidget(self.fill_thickness)
        layout_set.addRow("", hbox_fill)
        layout_set.addRow("", hbox_fill)
        GB_set.setLayout(layout_set)

        # # Рамка №2
        layout_sharpness = QtWidgets.QFormLayout(self)
        GB_sharpness = QtWidgets.QGroupBox('Сетка расчета риска')
        GB_sharpness.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_sharpness.addRow("", self.sharpness)
        GB_sharpness.setLayout(layout_sharpness)

        # # Рамка №2
        layout_shutdown = QtWidgets.QFormLayout(self)
        GB_shutdown = QtWidgets.QGroupBox('Время отключения, сек.')
        GB_shutdown.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_shutdown.addRow("", self.shutdown_time)
        GB_shutdown.setLayout(layout_shutdown)

        # Собираем рамки №№ 1
        tab_settings.layout.addWidget(GB_set)
        tab_settings.layout.addWidget(GB_sharpness)
        tab_settings.layout.addWidget(GB_shutdown)

        # Размещаем на табе рамки №№ 1
        tab_settings.setLayout(tab_settings.layout)
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

        self.table_data = QtWidgets.QTableWidget(0, 33)
        self.table_data_view()  # фукция отрисовки заголовков таблицы
        self.table_data.clicked[QtCore.QModelIndex].connect(self.get_index_in_table)
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
        self.draw_obj.setStyleSheet("text-align: left;")
        self.draw_obj.setToolTip('Указать координаты выбранного в таблице объекта')
        self.draw_obj.setIcon(object_ico)
        self.draw_obj.clicked.connect(self.change_draw_obj)
        self.draw_obj.setCheckable(True)
        self.draw_obj.setChecked(False)

        self.del_last_coordinate = QtWidgets.QPushButton("")
        self.del_last_coordinate.setToolTip('Удалить последнюю координату')
        self.del_last_coordinate.setIcon(minus_ico)
        self.del_last_coordinate.clicked.connect(self.delete_last_coordinate)

        self.del_all_coordinate = QtWidgets.QPushButton("")
        self.del_all_coordinate.setToolTip('Удалить все координаты')
        self.del_all_coordinate.setIcon(dbl_minus_ico)
        self.del_all_coordinate.clicked.connect(self.delete_all_coordinates)

        self.save_table = QtWidgets.QPushButton("Сохранить объекты")
        self.save_table.setToolTip('Сохранить объекты в базу данных')
        self.save_table.setIcon(save_ico)
        self.save_table.clicked.connect(self.save_table_in_db)

        layout_control.addRow("", self.add_row)
        layout_control.addRow("", self.del_row)
        layout_control.addRow("", self.example_obj)
        layout_control.addRow("", self.draw_obj)
        hbox_coordinate = QtWidgets.QHBoxLayout()
        hbox_coordinate.addWidget(self.del_last_coordinate)
        hbox_coordinate.addWidget(self.del_all_coordinate)
        layout_control.addRow("", hbox_coordinate)
        layout_control.addRow("", self.save_table)
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
        plan_add.triggered.connect(self.plan_add_func)
        plan_menu.addAction(plan_add)
        plan_replace = QtWidgets.QAction(replace_ico, 'Заменить', self)
        plan_replace.setStatusTip('Заменить план объекта')
        plan_replace.triggered.connect(self.plan_replace)
        plan_menu.addAction(plan_replace)
        plan_save = QtWidgets.QAction(save_ico, 'Coхранить', self)
        plan_save.setStatusTip('Сохранить текущее изображение плана объекта как файл')
        plan_save.triggered.connect(self.plan_save)
        plan_menu.addAction(plan_save)
        plan_clear = QtWidgets.QAction(clear_ico, 'Очистить', self)
        plan_clear.setStatusTip('Очистить план объекта')
        # plan_clear.triggered.connect(self.plan_clear)
        plan_menu.addAction(plan_clear)
        plan_del = QtWidgets.QAction(del_ico, 'Удалить план с объектами', self)
        plan_del.setStatusTip('Удалить изображение плана объекта')
        # plan_del.triggered.connect(self.plan_del)
        plan_menu.addAction(plan_del)

        # Выход из приложения
        exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_prog.setShortcut('Ctrl+Q')
        exit_prog.setStatusTip('Выход из Painter')
        # exit_prog.triggered.connect(self.close_event)

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
        help_menu = menubar.addMenu('Справка')
        help_menu.addAction(help_show)
        help_menu.addAction(about_prog)
        # Установить статусбар
        self.statusBar()
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        if not parent:
            self.show()

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Группа функций работы с таблицей self.table_data
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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

        header_list_tech = ['Длина, км', 'Диаметр, мм', 'Давление, МПа',
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
                           'Qсг, кДж/кг', 'sigma, -', 'Энергозапас, -', 'S, млн.руб/т', 'НКПР, об.%']

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
        self.del_all_item()

    def del_in_table(self):
        index = self.table_data.currentIndex()
        self.table_data.removeRow(index.row())

    def add_example_obj(self):

        data_list = [
            [f'Е-{random.randint(1, 20)}', 'Емкость', 'Наземная', 'Сталь', 'ДНС-2', 'Хранение нефти',
             '0', '0', '0,8', '10', f'{random.randrange(100, 500, 100)}', '0.8 ', f'{random.randrange(100, 500, 25)}',
             '1',
             '5', '0.1', '850', '3.25', '210', '65', '-28', '430', '3', '3', '46000', '7', '2', '0.6', '2.9',
             '1', '3', '0.33', ],
            [f'Нефтепровод от т.{random.randint(1, 20)} до УПСВ', 'Нефтепровод', 'Поздемная', 'Сталь В20',
             'Ивинское м.н.', 'Транспорт нефти',
             '0,985', f'{random.choice([89, 114, 159, 219])}', '1.25', '10', '0', '0 ', '0', '0',
             '5', '0.1', '850', '3.25', '210', '65', '-28', '430', '3', '4', '46000', '7', '2', '0.6', '2.9',
             '1', '3', '0.33', ]
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

    def delete_last_coordinate(self):
        # Удалить все линии и точки с ген.плана
        self.del_all_item()
        if self.row_ind_in_data_grid is not None:
            # Если ячейка крайнего столбца не пуста
            if self.table_data.item(self.row_ind_in_data_grid,
                                    self.table_data.columnCount() - 1) is not None:
                # очистим список координат для отрисовки
                self.data_draw_point.clear()
                # считаем кооординаты
                self.data_draw_point.extend(eval(self.table_data.item(self.row_ind_in_data_grid,
                                                                      self.table_data.columnCount() - 1).text()))
                # Удалим последнюю точку (х,у)
                self.data_draw_point = self.data_draw_point[:-2]
                # отрисуем все точки
                self.draw_all_item(self.data_draw_point)
                # Запишем новые координаты после удаления в таблицу
                widget_item_for_table = QtWidgets.QTableWidgetItem(str(self.data_draw_point))
                self.table_data.setItem(self.row_ind_in_data_grid,
                                        self.table_data.columnCount() - 1,
                                        widget_item_for_table)
                # очистим список координат для отрисовки
                self.data_draw_point.clear()

    def delete_all_coordinates(self):
        # Удалить все линии и точки с ген.плана
        self.del_all_item()
        if self.row_ind_in_data_grid is not None:
            # Если ячейка крайнего столбца не пуста
            if self.table_data.item(self.row_ind_in_data_grid,
                                    self.table_data.columnCount() - 1) is not None:
                # очистим список координат для отрисовки
                self.data_draw_point.clear()
                # Запишем пустые координаты после удаления в таблицу
                widget_item_for_table = QtWidgets.QTableWidgetItem(str([]))
                self.table_data.setItem(self.row_ind_in_data_grid,
                                        self.table_data.columnCount() - 1,
                                        widget_item_for_table)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # Группа функций для работы с базой данных
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    def db_create(self):
        self.db_name, self.db_path = class_db.Data_base(self.db_name, self.db_path).db_create()
        self.connect_info(self.db_name, self.db_path)

    def db_connect(self):
        self.db_name, self.db_path = class_db.Data_base(self.db_name, self.db_path).db_connect()
        self.connect_info(self.db_name, self.db_path)
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)
        self.del_all_item()  # очистить ген.планы от item

    def connect_info(self, name: str, path: str):
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

    # Функции локальной базы данных
    def delete_organization(self):
        # Текущая организиция
        current_org = self.organization.currentText()
        class_db.Data_base('local_base.db', str(PATH_LOCAL_BASE)).del_organization(current_org)
        # Очистить и заполнить организации заново
        self.organization.clear()
        self.organization.addItems(class_db.Data_base('local_base.db', str(PATH_LOCAL_BASE)).get_organizations())

    def edit_organization(self):
        self.edition = Edit_table_org()
        self.edition.show()

    # Функции работы с ген.планом
    def plan_add_func(self):
        class_db.Data_base(self.db_name, self.db_path).plan_add()
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)

    def plan_save(self):
        """
        Сохранение текущего вида ген.плана
        """
        text = str(int(time.time()))
        # self.del_all_item()
        self.scene.clearSelection()
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        image = QtGui.QImage(self.scene.sceneRect().size().toSize(), QtGui.QImage.Format_ARGB32)
        image.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(image)
        self.scene.render(painter)
        image.save((f"{self.db_path}/{text}.jpg"), "JPG")
        painter.end()

    def plan_replace(self):
        class_db.Data_base(self.db_name, self.db_path).plan_replace(self.plan_list.currentText())
        class_db.Data_base(self.db_name, self.db_path).plan_list_update(self.plan_list)
        self.plan_list_select(self.plan_list.currentText())

    def plan_list_select(self, text):

        self.scale_plan.setText('')
        self.result_type_act.setText('')

        data, image_data = class_db.Data_base(self.db_name, self.db_path).get_plan_in_db(text)
        # 1. Ген.план
        if image_data is not None:
            self.scene.clear()
            qimg = QtGui.QImage.fromData(image_data)
            self.pixmap = QtGui.QPixmap.fromImage(qimg)
            self.scene.addPixmap(self.pixmap)
            self.scene.setSceneRect(QtCore.QRectF(self.pixmap.rect()))

        # 2. Данные для таблицы
        # 2.1. Удалить данные из таблицы
        self.table_data.setRowCount(0)
        if len(data) != 0:
            # 3.1. Установить масштаб
            data = eval(data)
            self.scale_plan.setText(data.pop())  # крайний элемент списка всегда масштаб
            # 3.2. Заполнить таблицу
            for obj in data:
                count_row = self.table_data.rowCount()  # посчитаем количество строк
                self.table_data.insertRow(count_row)
                col = 0
                for item in obj:
                    # Запишем новые координаты после удаления в таблицу
                    widget_item_for_table = QtWidgets.QTableWidgetItem(item)
                    self.table_data.setItem(count_row, col,
                                            widget_item_for_table)
                    col += 1

    def save_table_in_db(self):
        """
        Функция сохранения информации в базу данных из таблицы данных
        """
        # Проверки перед сохранением
        self.is_action_valid()  # проверки

        # Проверки пройдены, можно запоминать данные:
        class_db.Data_base(self.db_name, self.db_path).save_data_in_db(self.plan_list.currentText(),
                                                                       self.scale_plan.text(),
                                                                       self.table_data)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Функции работы со сценой
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    def scene_press_event(self, event):
        # Проверим наличие ген.плана
        if self.plan_list.currentText() != '--Нет ген.планов--':

            # Проверим нажатие кнопки draw_type_act,
            # что мы хотим определить
            # - масштаб
            # - измерить растояние
            # - определить площадь:
            if self.draw_type_act.isChecked():
                # Отожмем кнопку отрисовки координатов объектов
                self.draw_obj.setChecked(False)
                # если масштаб
                if self.type_act.currentIndex() == 0:
                    print('draw scale')
                    self.data_draw_point.append(str(event.scenePos().x()))  # замеряем координаты клика
                    self.data_draw_point.append(str(event.scenePos().y()))  # и запсываем в data_draw_point
                    self.draw_all_item(self.data_draw_point)
                    if len(self.data_draw_point) == 4:  # как только длина data_draw_point == 4
                        num_int, ok = QtWidgets.QInputDialog.getInt(self, "Масштаб", "Сколько метров:")
                        if ok and num_int > 0:
                            x_a = float(self.data_draw_point[0])  # по координатам двух точек
                            y_a = float(self.data_draw_point[1])  # вычисляем расстояние в пикселях
                            x_b = float(self.data_draw_point[2])
                            y_b = float(self.data_draw_point[3])

                            length = LineString([(x_a, y_a), (x_b, y_b)]).length
                            self.data_draw_point.clear()  # очищаем data_draw_point
                            self.result_type_act.setText(f"В отрезке {num_int} м: {round(length, 2)} пикселей")
                            self.scale_plan.setText(f"{float(length) / num_int:.3f}")
                            self.draw_type_act.setChecked(False)
                            self.del_all_item()
                        elif ok and num_int <= 0:
                            self.data_draw_point.clear()  # очищаем data_draw_point
                            self.draw_type_act.setChecked(False)
                            self.del_all_item()
                            self.result_type_act.clear()
                            self.scale_plan.clear()
                        elif not ok:
                            self.data_draw_point.clear()  # очищаем data_draw_point
                            self.draw_type_act.setChecked(False)
                            self.del_all_item()
                            self.result_type_act.clear()
                            self.scale_plan.clear()

                    elif len(self.data_draw_point) > 4:
                        self.data_draw_point.clear()  # очищаем data_draw_point
                        self.draw_type_act.setChecked(False)
                        self.del_all_item()

                # если длина
                elif self.type_act.currentIndex() == 1:
                    print('draw lenght')
                    self.del_all_item()  # удалим все Item
                    if self.scale_plan.text() == "":  # проверим есть ли масштаб
                        msg = QtWidgets.QMessageBox(self)
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setWindowTitle("Информация")
                        msg.setText("Не установлен масштаб")
                        msg.exec()
                        self.draw_type_act.setChecked(False)
                        return
                    self.data_draw_point.append(str(event.scenePos().x()))  #
                    self.data_draw_point.append(str(event.scenePos().y()))
                    self.draw_all_item(self.data_draw_point)

                    copy_ = self.data_draw_point.copy()
                    if len(copy_) > 2:
                        i = 0
                        get_tuple = []
                        while i < len(copy_):
                            tuple_b = (float(copy_[i]), float(copy_[i + 1]))
                            get_tuple.append(tuple_b)
                            i += 2
                            if i == len(copy_):
                                break
                        length = LineString(get_tuple).length  # shapely
                        real_lenght = float(length) / float(self.scale_plan.displayText())
                        real_lenght = round(real_lenght, 2)
                        self.result_type_act.setText(f'Длина линии {real_lenght}, м')
                #  если площадь
                elif self.type_act.currentIndex() == 2:
                    print('draw square')
                    self.del_all_item()  # удалим все Item
                    if self.scale_plan.text() == "":  # проверим есть ли масштаб
                        msg = QtWidgets.QMessageBox(self)
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setWindowTitle("Информация")
                        msg.setText("Не установлен масштаб")
                        self.draw_type_act.setChecked(False)
                        msg.exec()
                        return
                    self.data_draw_point.append(str(event.scenePos().x()))  #
                    self.data_draw_point.append(str(event.scenePos().y()))

                    self.draw_all_item(self.data_draw_point)

                    copy_ = self.data_draw_point.copy()
                    if len(copy_) > 4:
                        i = 0
                        get_tuple = []
                        while i < len(copy_):
                            tuple_b = (float(copy_[i]), float(copy_[i + 1]))
                            get_tuple.append(tuple_b)
                            i += 2
                            if i == len(copy_):
                                break
                        area = Polygon(get_tuple).area  # shapely
                        real_area = float(area) / pow(float(self.scale_plan.displayText()), 2)
                        real_area = round(real_area, 2)
                        self.result_type_act.setText(f'Площадь {real_area}, м2')

            # Если нажата кнопка "Координаты"
            elif self.draw_obj.isChecked():
                print('here')
                # Отожмем кнопку отрисовки масштаба
                self.draw_type_act.setChecked(False)
                # Если выбрана сторока, то запишем координаты
                if self.row_ind_in_data_grid is not None:
                    print('write')
                    # если в крайней колонке пусто,то запишем координаты
                    if self.table_data.item(self.row_ind_in_data_grid,
                                            self.table_data.columnCount() - 1) is None:

                        self.data_draw_point.clear()

                        self.data_draw_point.append(str(event.scenePos().x()))  # замеряем координаты клика
                        self.data_draw_point.append(str(event.scenePos().y()))  # и запсываем в data_draw_point

                        widget_item_for_table = QtWidgets.QTableWidgetItem(str(self.data_draw_point))
                        self.table_data.setItem(self.row_ind_in_data_grid,
                                                self.table_data.columnCount() - 1,
                                                widget_item_for_table)
                        self.draw_all_item(self.data_draw_point)
                        self.data_draw_point.clear()
                    # если не пусто то к списку из ячейки будем добавлять координаты
                    else:
                        self.data_draw_point.clear()

                        self.data_draw_point.extend(eval(self.table_data.item(self.row_ind_in_data_grid,
                                                                              self.table_data.columnCount() - 1).text()))
                        self.data_draw_point.append(str(event.scenePos().x()))  # замеряем координаты клика
                        self.data_draw_point.append(str(event.scenePos().y()))  # и запсываем в data_draw_point

                        widget_item_for_table = QtWidgets.QTableWidgetItem(str(self.data_draw_point))
                        self.table_data.setItem(self.row_ind_in_data_grid,
                                                self.table_data.columnCount() - 1,
                                                widget_item_for_table)
                        self.draw_all_item(self.data_draw_point)
                        self.data_draw_point.clear()
                else:
                    self.draw_obj.setChecked(False)

    def del_all_item(self):
        """
        Удаляет все Item с картинки
        """
        # Находим все items на scene и переберем их
        for item in self.scene.items():  # удалить все линии точки и линии
            # Имя item
            name_item = str(item)
            # print(name_item)

            if name_item.find('QGraphicsLineItem') != -1:
                self.scene.removeItem(item)
            elif name_item.find('point') != -1:
                self.scene.removeItem(item)

    def draw_all_item(self, coordinate):
        """
        Рисует все Item на картинке
        """
        if coordinate == []:
            return
        i = 0
        k = 0
        while i < len(coordinate):
            thickness_marker = int(self.thickness_line.value() * 5)  # сторона маркера должна быть в 4 раза больше
            name_rings = Object_point(thickness_marker)
            name_rings.setPos(float(coordinate[i]), float(coordinate[i + 1]))
            self.scene.addItem(name_rings)
            i += 2
        while k < len(coordinate) - 2:
            line = QtWidgets.QGraphicsLineItem(float(coordinate[k]), float(coordinate[k + 1]),
                                               float(coordinate[k + 2]), float(coordinate[k + 3]))
            line.setPen(QtGui.QPen(QtCore.Qt.blue, self.thickness_line.value()))
            self.scene.addItem(line)
            k -= 2
            k += 4

    def plan_report_draw(self):
        print('plan draw')
        # Проверки
        self.is_action_valid()
        # 1. Получить что нужно рисовать?
        plan_report_index = self.plan_report_type.currentIndex()
        # Получить объекты
        # 2. Считаем данные из таблицы
        data_list = self.get_data_in_table()

        if plan_report_index == 4:
            # риск
            print("draw risk")
            self.draw_risk(data_list)

        else:
            result = class_data_draw.Data_draw().data_for_zone(data_list, plan_report_index, self.shutdown_time.value())
            #   Нарисуем зоны поражения
            self.draw_from_data(result, fill_thickness = self.fill_thickness.value())

    def draw_from_data(self, data: list, fill_thickness:int):
        '''
        Функция отрисовки на ген плане зон поражения.
        :param data список вида [[1,2,3,4,5,6],[1,2,3,4,5,6]..n]
                    количество списков = количетву отрисовываемых объектов .

        '''

        # print(data)
        # 1. Проверки
        # 1.1. Проверки на заполненность данных
        self.is_action_valid()
        # 1.2. Список данных должен быть не пустой
        if len(data) == 0:
            return

        # 2. Получить данные
        # 2.1. О масштабе
        scale_plan = float(self.scale_plan.text())
        # 2.2. Получить координаты и типы объектов
        type_obj = []
        coordinate_obj = []
        for row in range(0, self.table_data.rowCount()):  # получим типы объектов
            type_obj.append(int(self.table_data.item(row, 13).text()))
            coordinate_obj.append(eval(self.table_data.item(row,
                                                            self.table_data.columnCount() - 1).text()))

        # 3. Нарисовать
        # 3.1. Определим все цвета зон покнопкам
        color_zone_arr = self.get_color_for_zone()

        # 3.2. Отрисовка зон
        # На основе исходной картинки создадим QImage и QPixmap
        _, image_data = class_db.Data_base(self.db_name, self.db_path).get_plan_in_db(self.plan_list.currentText())
        qimg = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        pixmap_zone = QtGui.QPixmap(pixmap.width(), pixmap.height())
        pixmap_zone.fill(QtGui.QColor(255, 255, 255, 255))
        # Создадим QPainter
        qp = QtGui.QPainter(pixmap_zone)
        # Начнем рисование
        qp.begin(pixmap_zone)

        for zone_index in range(-1, -7, -1):
            i = 0  # итератор для объектов
            k = 0  # итератор для объектов без заливки
            for obj in type_obj:
                # # начинаем рисовать с последнего цвета
                color = color_zone_arr[zone_index]
                zone = math.fabs(float(data[i][zone_index]) * scale_plan * 2)  # т.к. на вход радиус, а нужен диаметр
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

                # возьмем координаты оборудования
                obj_coord = self.get_polygon(coordinate_obj[i])
                if len(obj_coord) >= 2:  # координаты можно преобразовать в полигон

                    if obj == 0:
                        # линейн. получим полигон
                        qp.drawPolyline(obj_coord)
                    else:
                        # стац. об. получим полигон
                        qp.drawPolyline(obj_coord)
                        qp.drawPolygon(obj_coord, QtCore.Qt.OddEvenFill)
                else:  # не получается полигон, значит точка
                    pen_point = QtGui.QPen(QtGui.QColor(color[0], color[1], color[2], color[3]), 1, QtCore.Qt.SolidLine)
                    qp.setPen(pen_point)
                    point = QtCore.QPoint(int(float(coordinate_obj[i][0])), int(float(coordinate_obj[i][1])))
                    qp.drawEllipse(point, zone / 2, zone / 2)  # т.к. нужен радиус

                i += 1  # следующий объект

            # Рисуем прозрачные

            if fill_thickness != 0:
                for obj in reversed(type_obj):
                    zone_without_fill = math.fabs(
                        float(data[k][zone_index]) * scale_plan * 2) - fill_thickness

                    # определим ручку и кисточку
                    pen_without_fill = QtGui.QPen(QtGui.QColor(255, 255, 255, 255), zone_without_fill,
                                                  QtCore.Qt.SolidLine)
                    brush_without_fill = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
                    # со сглаживаниями
                    pen_without_fill.setJoinStyle(QtCore.Qt.RoundJoin)
                    # закругленный концы
                    pen_without_fill.setCapStyle(QtCore.Qt.RoundCap)
                    qp.setPen(pen_without_fill)
                    qp.setBrush(brush_without_fill)

                    # возьмем координаты оборудования
                    obj_coord = self.get_polygon(coordinate_obj[k])
                    if len(obj_coord) >= 2:  # координаты можно преобразовать в полигон

                        if obj == 0:
                            # линейн. получим полигон
                            qp.drawPolyline(obj_coord)
                        else:
                            # стац. об. получим полигон
                            qp.drawPolyline(obj_coord)
                            qp.drawPolygon(obj_coord, QtCore.Qt.OddEvenFill)
                    else:  # не получается полигон, значит точка
                        pen_point = QtGui.QPen(QtGui.QColor(255, 255, 255, 255), 1,
                                               QtCore.Qt.SolidLine)
                        qp.setPen(pen_point)
                        point = QtCore.QPoint(int(float(coordinate_obj[k][0])), int(float(coordinate_obj[k][1])))
                        qp.drawEllipse(point, zone_without_fill / 2, zone_without_fill / 2)  # т.к. нужен радиус

                    k += 1  # следующий объект



        # Завершить рисование
        qp.end()
        # удалить белый фон (при наличии)
        pixmap_zone = class_data_draw.Data_draw().del_white_pixel(pixmap_zone)
        # Положим одну картинку на другую
        painter = QtGui.QPainter(pixmap)
        painter.begin(pixmap)
        painter.setOpacity(self.opacity.value())
        painter.drawPixmap(0, 0, pixmap_zone)
        painter.end()
        # Разместим на сцене pixmap с pixmap_zone
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

    def draw_risk(self, data_list):
        """Рисование риска"""
        self.is_action_valid()
        # достаем картинку из БД
        _, image_data = class_db.Data_base(self.db_name, self.db_path).get_plan_in_db(self.plan_list.currentText())

        # На основе исходной картинки создадим QImage и QPixmap
        qimg = QtGui.QImage.fromData(image_data)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        # создадим соразмерный pixmap_zone и сделаем его прозрачным
        width, height = pixmap.width(), pixmap.height()
        pixmap_zone = QtGui.QPixmap(width, height)
        pixmap_zone.fill(QtGui.QColor(0, 0, 0, 0))
        qimg_zone = pixmap_zone.toImage()

        # сделаем нулевую матрицу по размерам картинки
        zeors_array = np.zeros((width, height))
        # получим пробиты и расстояния
        expl_all_probit, strait_all_probit, flash_all_probit, scenarios_all = class_data_draw.Data_draw().data_for_risk(
            data_list, self.shutdown_time.value())

        # Рассчитаем тепловую карту
        sharpness = int(self.sharpness.value())
        calc_array = class_data_draw.Data_draw().calc_heat_map(sharpness, zeors_array, data_list, width, height,
                                                               0.3, expl_all_probit,
                                                               # вместо 1 должно быть !!! float(self.scale_plan.text())
                                                               strait_all_probit, flash_all_probit, scenarios_all)

        # Нарисуем тепловую карту
        heat_map = class_data_draw.Data_draw().show_heat_map(calc_array, width, height, qimg_zone)
        pixmap_zone = QtGui.QPixmap.fromImage(heat_map)
        # Положим одну картинку на другую
        painter = QtGui.QPainter(pixmap)
        painter.begin(pixmap)
        painter.setOpacity(self.opacity.value())
        painter.drawPixmap(0, 0, pixmap_zone)
        painter.end()
        # Разместим на сцене pixmap с pixmap_zone
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(QtCore.QRectF(pixmap.rect()))

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
        self.draw_obj.setChecked(False)
        self.draw_type_act.setChecked(False)
        if self.view.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        else:
            self.view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    # Функции отчетов
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    def report_word(self):
        # 1. Получить количество ген.планов в базе данных
        plan_count = self.plan_list.count()
        print(plan_count)

        # Диалог нужны ли планы
        dlg = QtWidgets.QMessageBox(self)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        dlg.setWindowTitle("Нарисовать...")
        dlg.setText("Нарисовать ген.планы?")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:

            for i in range(plan_count):
                # Выбрать ген.план
                self.plan_list.setCurrentIndex(i)
                # Установить ген.план
                self.plan_list_select(text=self.plan_list.currentText())
                # отрисовка зон
                for j in range(5):
                    # Установить тип аварии (взрыв, пожар...риск)
                    self.plan_report_type.setCurrentIndex(j)
                    # Нарисовать
                    if self.scale_plan.text() == '':
                        continue
                    data_table = self.get_data_in_table()
                    if '' in data_table:
                        continue
                    self.plan_report_draw()
                    # Сохранить
                    self.plan_save()
                    time.sleep(2)  # что бы успел сохранить рисунок

        # Диалог нужен ли текст
        dlg = QtWidgets.QMessageBox(self)
        dlg.setIcon(QtWidgets.QMessageBox.Question)
        dlg.setWindowTitle("Заполнить...")
        dlg.setText("Заполнить текстовые шаблоны?")
        dlg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button = dlg.exec()

        if button == QtWidgets.QMessageBox.Yes:

            # Информация из базы данных
            current_org = self.organization.currentText()
            info_about_organization = class_db.Data_base('local_base.db',
                                                         str(PATH_LOCAL_BASE)).get_info_about_organizations(current_org)
            print(info_about_organization, "info_about_organization")
            if info_about_organization == None:
                return
            #  Заполнение шаблона
            dangerous_object = class_opo.Dangerous_object()
            for i in range(plan_count):
                # Выбрать ген.план
                self.plan_list.setCurrentIndex(i)
                # Установить ген.план
                self.plan_list_select(text=self.plan_list.currentText())
                # если не заполнена таблица и масштаб, то для плана ничего заполнять не надо
                data_table = self.get_data_in_table()
                if '' in data_table:
                    continue
                if self.scale_plan.text() == '':
                    continue

                for obj in data_table:
                    obj_dict = {
                        'name': str(obj[0]),
                        'name_full': str(obj[1]),
                        'located': str(obj[2]),
                        'material': str(obj[3]),
                        'ground': str(obj[4]),
                        'target': str(obj[5]),
                        'length': float(obj[6]),  # км
                        'diameter': float(obj[7]),  # мм
                        'pressure': float(obj[8]),  # кПа
                        'temperature': float(obj[9]),  # град.С
                        'volume': float(obj[10]),  # м3
                        'completion': float(obj[11]),  # - (степень заполнения)
                        'spill_square': float(obj[12]),  # м2 обвалование
                        'type': float(obj[13]),  # тип оборудования
                        'spreading': float(obj[14]),  # м^-1
                        'place': float(obj[15]),  # коэф.участия во взрыве
                        'density': float(obj[16]),  # кг/м3
                        'density_gas': float(obj[17]),  # кг/м3
                        'molecular_weight': float(obj[18]),  # кг/кмоль
                        'steam_pressure': float(obj[19]),  # кПа
                        'flash_temperature': float(obj[20]),  # град.С
                        'boiling_temperature': float(obj[21]),  # град.С
                        'class_substance': float(obj[22]),  # класс вещества по детонационной ячейки
                        'view_space': float(obj[23]),  # класс окрущающего пространства
                        'heat_of_combustion': float(obj[24]),  # кДж/кг
                        'sigma': float(obj[25]),  # -
                        'energy_level': float(obj[26]),  # -
                        'cost_sub': float(obj[27]),
                        'lower_concentration': float(obj[28]),
                        'death_person': float(obj[29]),
                        'injured_person': float(obj[30]),
                        'time_person': float(obj[31]),

                        'water_cut': FRACTIONS_OIL[0],  # %
                        'sulfur': FRACTIONS_OIL[1],  # %
                        'resins': FRACTIONS_OIL[2],  # % смолы
                        'asphalt': FRACTIONS_OIL[3],  # % асфальтены
                        'paraffin': FRACTIONS_OIL[4],  # %
                        'viscosity': FRACTIONS_OIL[5],  # МПа*с
                        'hydrogen_sulfide': FRACTIONS_OIL[6],  # % сероводород

                    }

                    dangerous_object.append_device(class_opo.Device(obj_dict, self.shutdown_time.value()))

            print(len(dangerous_object.list_device))
            if len(dangerous_object.list_device) != 0:
                dangerous_object.create_rpz(self.db_path, eval(info_about_organization[0]))

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    #  Прочие функции
    # 1. Нельзя одновременно рисовать объект
    # и измерять, например масштаб
    def change_draw_type_act(self):
        self.data_draw_point.clear()  # очистим координаты
        self.del_all_item()
        if self.draw_obj.isChecked():
            self.draw_obj.setChecked(False)

    def change_draw_obj(self):
        self.data_draw_point.clear()  # очистим координаты

        if self.draw_type_act.isChecked():
            self.draw_type_act.setChecked(False)
        # Если в таблице сторок нет, то запретить запоминать координаты
        if self.row_ind_in_data_grid == None:
            self.draw_obj.setChecked(False)

    # 2. При переключении действия очистить список координат и
    # удалить все item (точки и линии на плане)
    def select_type_act(self, text):
        self.data_draw_point.clear()  # очистим координаты
        self.del_all_item()

    def get_index_in_table(self, index):

        self.draw_type_act.setChecked(False)  # исключить измерение масштаба и пр.
        self.draw_obj.setChecked(False)  # исключить дорисовку предыдущего объекта.
        self.del_all_item()  # очистим координаты
        self.row_ind_in_data_grid = index.row()  # возьмем индек строки
        # Если ячейка крайнего столбца не пуста
        if self.table_data.item(self.row_ind_in_data_grid,
                                self.table_data.columnCount() - 1) is not None:
            # очистим список координат для отрисовки
            self.data_draw_point.clear()
            # считаем кооординаты
            self.data_draw_point.extend(eval(self.table_data.item(self.row_ind_in_data_grid,
                                                                  self.table_data.columnCount() - 1).text()))
            # отрисуем все точки
            self.draw_all_item(self.data_draw_point)
            # очистим список координат для отрисовки
            self.data_draw_point.clear()

    # 3. Выбор цвета для кнопок
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

    # 4. Получение данных из Excel
    def get_data_excel(self):
        """
        Получение данных из файла excel.
        Количество столбцов не более 6, т.к. зон всего 6
        Количество строк равно равно количеству объектов
        """
        self.is_action_valid()  # проверки

        try:
            wb = xw.books.active
            cellRange = wb.app.selection
            vals = cellRange.value
            if self.table_data.rowCount() != len(vals):
                self.data_excel.setText("")
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText("Строк в Excel больше чем объектов!")
                msg.exec()
                return
            elif len(vals[0]) != 6:
                self.data_excel.setText("")
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText("Столбцов в Excel больше чем зон поражения!")
                msg.exec()
                return
            else:
                self.data_excel.setText(str(vals))
        except:
            self.data_excel.setText("")
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Ошибка при считывании данных в Excel!")
            msg.exec()
            return

    # 5. Проверка наличия базы, генплана, масштаба, объектов и
    # их заполненности
    def is_action_valid(self):
        """
        Функция проверки наличия всех данных для корректной работы
        """
        # 1. Есть ли база данных
        if self.db_name == '' and self.db_path == '':
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет подключения к базе данных!")
            msg.exec()
            return
        # 2. Есть ли генплан
        if self.plan_list.currentText() == '--Нет ген.планов--':
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет ген.плана!")
            msg.exec()
            return
        # 3. Есть ли масштаб
        if self.scale_plan.text() == '':
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Не указан масштаб!")
            msg.exec()
            return
        # 4. Есть ли объекты в таблице
        if self.table_data.rowCount() == 0:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет объектов для сохранения!")
            msg.exec()
            return
        # 5. Есть ли пустые ячейки в таблице данных
        for i in range(self.table_data.rowCount()):
            for j in range(self.table_data.columnCount()):
                if self.table_data.item(i, j) is None:
                    msg = QtWidgets.QMessageBox(self)
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowTitle("Информация")
                    msg.setText("Не все данные таблицы заполнены!")
                    msg.exec()
                    return
        # 6. Правильно ли заполнены объемы емкостей / трубопроводов
        data_list = self.get_data_in_table()
        for obj in data_list:
            lenght = float(obj[6])
            volume = float(obj[10])
            if lenght == 0 and volume == 0:
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText(f"Объект{obj[0]}: нулевая длина и нулевой объем.")
                msg.exec()
                return
            if lenght != 0 and volume != 0:
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText(f"Объект{obj[0]}: заполнены характеристики длина и объем.")
                msg.exec()
                return

    # 6. Получить цвета зон поражающих факторов
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

    # 7. На основе координат создает по QPoint QPolygon
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

    def get_data_in_table(self):
        data_list = []
        count_row = 0  # начинаем с 0 строки
        for _ in range(0, self.table_data.rowCount()):  # посчитаем строки
            append_list = []  # заведем пустой список для объекта
            count_col = 0  # колонка с индесом 0
            for _ in range(0, self.table_data.columnCount()):  # для каждого столбца строки

                if count_col != self.table_data.columnCount() - 1:
                    var = self.table_data.item(count_row, count_col).text().replace(',', '.')
                else:
                    var = self.table_data.item(count_row, count_col).text()
                append_list.append(var)  # добавим в словарь текст ячейки
                count_col += 1  # + 1 к столбцу
            data_list.append(append_list)  # добавим объект
            count_row += 1  # +1 к строке (новая строка если len(data_list) > 1)
        return data_list
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    locale = 'ru_RU'
    qt_translator = QtCore.QTranslator(app)
    qt_translator.load('{}/qtbase_{}.qm'.format(I18N_QT_PATH, locale))
    app_translator = QtCore.QTranslator(app)
    app_translator.load('{}/{}.qm'.format(I18N_QT_PATH, locale))
    app.installTranslator(qt_translator)
    app.installTranslator(app_translator)
    ex = Painter()
    app.exec_()
