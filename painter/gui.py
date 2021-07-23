# -----------------------------------------------------------
# Графический интерфейс предназначен для отрисовки зон действия
# поражающих факторов и построения полей потенциального риска
# на основе данных из excel (расчеты в данном модуле не производятся)
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import sqlite3
import time
import sys
import os
from pathlib import Path
from PySide2 import QtWidgets, QtGui, QtCore



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
        self.type_act = QtWidgets.QComboBox()
        self.type_act.addItems(["Объект", "Масштаб", "Расстояние", "Площадь"])
        self.type_act.setItemIcon(0, object_ico)
        self.type_act.setItemIcon(1, scale_ico)
        self.type_act.setItemIcon(2, dist_ico)
        self.type_act.setItemIcon(3, area_ico)
        self.result_lbl = QtWidgets.QLabel()
        self.draw_btn = QtWidgets.QPushButton("Применить")
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
        self.obj_save_btn = QtWidgets.QPushButton("Сохранить")
        self.obj_save_btn.setIcon(save_ico)
        self.obj_save_btn.setToolTip("Сохранить объект")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)

        # Рамка №4 (то что будет в рамке 4)
        self.model = QtGui.QStandardItemModel(0, 0)  # Создаем модель QStandardItemModel для QTreeView
        self.all_items = QtGui.QStandardItem("Объекты:")  #
        self.all_items.setIcon(tree_ico)
        self.model.appendRow(self.all_items)
        self.view_tree = QtWidgets.QTreeView()
        self.view_tree.header().hide()
        self.view_tree.setModel(self.model)
        # self.view_tree.clicked.connect(self.treefunction)

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
        GB_obj = QtWidgets.QGroupBox('Действие')
        GB_obj.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_obj.addRow("", self.obj_name)
        layout_obj.addRow("", self.obj_coord)
        layout_obj.addRow("", self.obj_type)
        layout_obj.addRow("", self.obj_save_btn)
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
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        self.color_zone2_btn = QtWidgets.QPushButton("Зона 2")
        self.color_zone2_btn.setIcon(color_ico)
        self.color_zone2_btn.setToolTip("Цвет зоны 2")
        self.color_zone2_btn.setStyleSheet("background-color: blue")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        self.color_zone3_btn = QtWidgets.QPushButton("Зона 3")
        self.color_zone3_btn.setIcon(color_ico)
        self.color_zone3_btn.setToolTip("Цвет зоны 3")
        self.color_zone3_btn.setStyleSheet("background-color: orange")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        self.color_zone4_btn = QtWidgets.QPushButton("Зона 4")
        self.color_zone4_btn.setIcon(color_ico)
        self.color_zone4_btn.setToolTip("Цвет зоны 4")
        self.color_zone4_btn.setStyleSheet("background-color: green")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        self.color_zone5_btn = QtWidgets.QPushButton("Зона 5")
        self.color_zone5_btn.setIcon(color_ico)
        self.color_zone5_btn.setToolTip("Цвет зоны 5")
        self.color_zone5_btn.setStyleSheet("background-color: magenta")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        self.color_zone6_btn = QtWidgets.QPushButton("Зона 6")
        self.color_zone6_btn.setIcon(color_ico)
        self.color_zone6_btn.setToolTip("Цвет зоны 6")
        self.color_zone6_btn.setStyleSheet("background-color: yellow")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)
        # Рамка №4 (то что будет в рамке 4)
        self.data_excel = QtWidgets.QLineEdit()
        self.data_excel.setPlaceholderText("Данные из Excel")
        self.data_excel.setToolTip("Данные из Excel")
        self.data_excel.setReadOnly(True)
        self.get_data_btn = QtWidgets.QPushButton("Загрузить")
        self.get_data_btn.setIcon(excel_ico)
        self.get_data_btn.setToolTip("Загрузить выделенный диапазон")
        # self.obj_save_btn.clicked.connect(self.on_picture_draw)

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

        # Размещаем на табе
        self.tab_settings.layout.addWidget(GB_db)
        self.tab_settings.layout.addWidget(GB_plan)
        self.tab_settings.layout.addWidget(GB_zone)
        self.tab_settings.layout.addWidget(GB_xl)
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
        if self.db_name.text() == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет подключенной базы данных")
            msg.exec()
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
        if self.db_name.text() == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Нет подключенной базы данных")
            msg.exec()
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
        if self.plan_list.currentText() == "--Нет ген.планов--":
            return
        self.plan_list_select(text=self.plan_list.currentText())

    def plan_del(self):
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
        # Convert digital data to binary format
        with open(file_path, 'rb') as file:
            blobData = file.read()
        return blobData

    def plan_list_select(self, text):
        # self.reset_state_obj()  # обнуляем все поля
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

        # # Очищаем словарь объектов
        # self.data_obj.clear()
        # # достаем словарь из БД
        # sqliteConnection = sqlite3.connect(path_str)
        # cursorObj = sqliteConnection.cursor()
        # cursorObj.execute("SELECT * FROM objects")
        # data_in_db = cursorObj.fetchall()
        # for row in data_in_db:
        #     if str(row[3]) + ',' + str(row[0]) == text:
        #         if str(row[1]) == "":
        #             self.data_obj = {}
        #         else:
        #             self.data_obj = eval(row[1])
        # sqliteConnection.execute("VACUUM")
        # cursorObj.close()
        # # Удаляем все позиции из объектов
        # self.all_items.removeRows(0, self.all_items.rowCount())
        # # # добавить из списка self.data_obj  объекты
        # # for key in self.data_obj.keys():
        # #     key = QStandardItem(key)
        # #     self.all_items.setChild(self.all_items.rowCount(), key)

    def plan_list_update(self):
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
    ex = Painter()
    app.exec_()
