# -----------------------------------------------------------
# Графический интерфейс предназначен для взаимодействия с БД
# объектов для ОПО нефтедобычи
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from PySide2 import QtSql
from PySide2 import QtWidgets
from PySide2 import QtCore


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Input Dialog')
        self.line_edit_name = QtWidgets.QLineEdit()
        self.line_edit_quantity = QtWidgets.QLineEdit()
        self.line_edit_category = QtWidgets.QLineEdit()

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Name:', self.line_edit_name)
        form_layout.addRow('quantity:', self.line_edit_quantity)
        form_layout.addRow('category:', self.line_edit_category)

        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)


class Storage_app(QtWidgets.QMainWindow):
    """
    Основной класс базы данных реализующий представление
    базы данных ОПО
    """
    def __init__(self):
        super().__init__()

        self.createConnection() # проверка подключения базы данных
        self.fillTable()  # !!! тестовое заполнение базы данных
        self.createModel() # создание модели
        self.initUI() # отображение UI

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget) # установим центральный виждет как QWidget
        # Добавим кнопки
        btnAdd = QtWidgets.QPushButton("&Добавить запись")
        btnAdd.clicked.connect(self.addRecord)
        btnDel = QtWidgets.QPushButton("&Удалить запись")
        btnDel.clicked.connect(self.delRecord)
        # Упакуем все в QVBoxLayout
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)
        layout.addWidget(btnAdd)
        layout.addWidget(btnDel)

    def createConnection(self):
        """
        Проверка подключения к базе данных,
        1) если ее нет, то она создается
        2) если невозможно подключиться, то пишет в терминале
        "Cannot establish a database connection"
        """
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("local_base.db")  # !!! .db
        if not self.db.open():
            print("Cannot establish a database connection")
            return False

    def fillTable(self):
        """
        Вспомогательная функция заполнениия базы данных
        Отключить после тестового запуска
        """
        file_path = (f"{os.getcwd()}\\test_BLOB.jpg")
        test_BLOB = self.convertToBinaryData(file_path)
        test_BLOB = QtCore.QByteArray(test_BLOB)

        self.db.transaction()
        q = QtSql.QSqlQuery()
        #
        q.exec_("DROP TABLE IF EXISTS company;")
        q.exec_("CREATE TABLE company ("
                "id INT PRIMARY KEY, "
                "name_company TEXT NOT NULL, "
                "full_name_manager TEXT NOT NULL, "
                "ur_address TEXT NOT NULL, "
                "post_address TEXT NOT NULL, "
                "telephone TEXT NOT NULL, "
                "email TEXT NOT NULL, "
                "fax TEXT DECIMAL NULL, "
                "inn_number INT NOT NULL, "
                "kpp_number INT NOT NULL, "
                "ogrn_number INT NOT NULL, "
                "license_opo BLOB NOT NULL, "
                "reg_opo BLOB NOT NULL, "
                "position_pk BLOB NOT NULL, "
                "position_crash BLOB NOT NULL );")

        # Вставка тестовых значений
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, full_name_manager, "
                  "ur_address, post_address, telephone, email, fax, inn_number, kpp_number, ogrn_number, "
                  "license_opo, reg_opo, position_pk, position_crash) "
                      "VALUES (:id, :name_company, :full_name_manager, :ur_address,:post_address, :telephone, :email, "
                  ":fax, :inn_number, :kpp_number, :ogrn_number, :license_opo, :reg_opo, :position_pk, :position_crash)")

        query.bindValue(":id", 1)
        query.bindValue(":name_company", 'АО МЕЛЛЯНЕФТЬ')
        query.bindValue(":full_name_manager", 'Тазиев Марат Миргазиянович')
        query.bindValue(":ur_address", 'РФ, РТ, г. Альметьевск, пр-кт Строителей, д. 51')
        query.bindValue(":post_address", 'РФ, РТ, г. Альметьевск, пр-кт Строителей, д. 51')
        query.bindValue(":email", 'mellyaneft@tatais.ru')
        query.bindValue(":telephone", '8 (855) 337-22-60')
        query.bindValue(":fax", '8 (855) 337-22-61')
        query.bindValue(":inn_number", 1636002647)
        query.bindValue(":kpp_number", 164401001)
        query.bindValue(":ogrn_number", 1021605555179)
        query.bindValue(":license_opo", test_BLOB)
        query.bindValue(":reg_opo", test_BLOB)
        query.bindValue(":position_pk", test_BLOB)
        query.bindValue(":position_crash", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, full_name_manager, "
                      "ur_address, post_address, telephone, email, fax, inn_number, kpp_number, ogrn_number, "
                      "license_opo, reg_opo, position_pk, position_crash) "
                      "VALUES (:id, :name_company, :full_name_manager, :ur_address,:post_address, :telephone, :email, "
                      ":fax, :inn_number, :kpp_number, :ogrn_number, :license_opo, :reg_opo, :position_pk, :position_crash)")

        query.bindValue(":id", 2)
        query.bindValue(":name_company", 'АО ТАТОЙЛГАЗ')
        query.bindValue(":full_name_manager", 'Фассахов Роберт Харрасович')
        query.bindValue(":ur_address", 'РФ, РТ, г. Альметьевск, ул. Тухватуллина, 2а')
        query.bindValue(":post_address", 'РФ, РТ, г. Альметьевск, ул. Тухватуллина, 2а')
        query.bindValue(":email", 'reception@tatoilgas.ru')
        query.bindValue(":telephone", '8(8553) 314-110')
        query.bindValue(":fax", ' 8(8553) 314-218')
        query.bindValue(":inn_number", 1644011638)
        query.bindValue(":kpp_number", 164401001)
        query.bindValue(":ogrn_number", 1021601625561)
        query.bindValue(":license_opo", test_BLOB)
        query.bindValue(":reg_opo", test_BLOB)
        query.bindValue(":position_pk", test_BLOB)
        query.bindValue(":position_crash", test_BLOB)
        query.exec_()


        #                             vvv
        q.exec_("DROP TABLE IF EXISTS opo;")
        q.exec_("CREATE TABLE opo ("
                "id INT PRIMARY KEY, "
                "id_company INT NOT NULL, "
                "name_opo TEXT NOT NULL, "
                "address_opo TEXT NOT NULL, "
                "reg_number_opo TEXT NOT NULL, "
                "class_opo TEXT NOT NULL, "
                "reg_certificate BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO opo (id, id_company, name_opo, "
                  "address_opo, reg_number_opo, class_opo, reg_certificate)"
                  "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo, :reg_certificate)")

        query.bindValue(":id", 1)
        query.bindValue(":id_company", 1)
        query.bindValue(":name_opo", 'Фонд скважин Муслюмовского месторождения нефти и газа')
        query.bindValue(":address_opo", 'РФ, РТ, Муслюмовский, Азнакаевский и Сармановский районы')
        query.bindValue(":reg_number_opo", 'А43-01341-0005')
        query.bindValue(":class_opo", '3')
        query.bindValue(":reg_certificate", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO opo (id, id_company, name_opo, "
                  "address_opo, reg_number_opo, class_opo, reg_certificate)"
                  "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo, :reg_certificate)")

        query.bindValue(":id", 2)
        query.bindValue(":id_company", 2)
        query.bindValue(":name_opo", 'Фонд скважин Урмышлинского месторождения нефти')
        query.bindValue(":address_opo", 'РФ, РТ, Черемшанский район, Лениногорский районы')
        query.bindValue(":reg_number_opo", 'А43-01109-0001')
        query.bindValue(":class_opo", '3')
        query.bindValue(":reg_certificate", test_BLOB)
        query.exec_()

        self.db.commit()

    def createModel(self):
        """
        Создание модели для отображения
        """
        self.model = QtSql.QSqlRelationalTableModel()
        self.model.setTable("opo")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование организации")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Наименование ОПО")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Адрес ОПО")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Рег.номер ОПО")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Класс ОПО")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, "Свидетельство о регистрации")
        self.set_relation()
        self.model.select()

    def initUI(self):
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        mode = QtWidgets.QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)

    def closeEvent(self, event):
        if (self.db.open()):
            self.db.close()

    def set_relation(self):
        self.model.setRelation(1, QtSql.QSqlRelation(
            "company",
            "id",
            "name_company"
        ))

    def addRecord(self):
        inputDialog = Dialog()
        rez = inputDialog.exec()
        if not rez:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return

        name = inputDialog.line_edit_name.text()
        quantity = inputDialog.line_edit_quantity.text()
        category = inputDialog.line_edit_category.text()
        if (not name) or (not quantity) or (not category):
            msg = QtWidgets.QMessageBox.information(self,
                                          'Внимание', 'Заполните пожалуйста все поля.')
            return

        r = self.model.record()
        r.setValue(0, name)
        r.setValue(1, int(quantity))
        r.setValue(2, int(category))

        self.model.insertRecord(-1, r)
        self.model.select()

    def delRecord(self):
        row = self.view.currentIndex().row()
        if row == -1:
            msg = QtWidgets.QMessageBox.information(self,
                                          'Внимание', 'Выберите запись для удаления.')
            return

        name = self.model.record(row).value(0)
        quantity = self.model.record(row).value(1)
        category = self.model.record(row).value(2)

        inputDialog = Dialog()
        inputDialog.setWindowTitle('Удалить запись ???')
        inputDialog.line_edit_name.setText(name)
        inputDialog.line_edit_quantity.setText(str(quantity))
        inputDialog.line_edit_category.setText(str(category))
        rez = inputDialog.exec()
        if not rez:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return

        self.model.setRelation(2, QtSql.QSqlRelation())
        self.model.select()
        self.model.removeRow(row)
        self.set_relation()
        self.model.select()

        msg = QtWidgets.QMessageBox.information(self, 'Успех', 'Запись удалена.')

    def convertToBinaryData(self, file_path):
        # Конвертирование в BLOB
        with open(file_path, 'rb') as file:
            blobData = file.read()
            print()
        return blobData

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    w = Storage_app()
    w.setWindowTitle("Storage_sys")
    w.show()
    app.exec_()



# import sys
# import os
# from pathlib import Path
# from PySide2 import QtWidgets, QtGui, QtSql
#
# db = QtSql.QSqlDatabase("QSQLITE")
# db.setDatabaseName("data.db")
# db.open()
#
# class Storage_app(QtWidgets.QMainWindow):
#
#     def __init__(self, parent=None) -> None:
#         super().__init__()
#         # Создадим для добавления информации в базу данных
#         self.dialog_company_add = Company_add()
#
#         # Иконки
#         self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
#         company_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/company.png')
#         state_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/state.png')
#         ok_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/ok.png')
#         object_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/object.png')
#         doc_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/document.png')
#         line_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tube.png')
#         build_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/build.png')
#         project_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/project.png')
#         project2_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/project2.png')
#
#
#
#
#
#
#         replace_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/replace.png')
#         save_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
#         clear_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/clear.png')
#         # del_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/del.png')
#         question_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/question.png')
#         scale_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/scale.png')
#         dist_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/polyline.png')
#         area_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/area.png')
#         settings_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/settings.png')
#         draw_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/draw.png')
#         exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
#         info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
#         # Главное окно
#         self.setGeometry(300, 300, 750, 550)
#         self.setWindowTitle('Storage_app')
#         self.setWindowIcon(self.main_ico)
#         # Центральный виджет
#         # создаем сетку из двух колонок
#         # окно для графики
#         # окно для ввода данных
#         central_widget = QtWidgets.QWidget()
#         grid = QtWidgets.QGridLayout(self)
#         grid.setColumnStretch(0, 5)
#         grid.setColumnStretch(1, 2)
#         # В первой колонке создаем место под вид БД
#         self.table = QtWidgets.QTableView()
#         self.model = QtSql.QSqlRelationalTableModel(db=db)
#         self.table.setModel(self.model)
#         self.model.setTable("company")
#
#         # т.к. данных  много создадим
#         # вкладки табов
#         self.tabs = QtWidgets.QTabWidget()  # создаем вкладки табов
#         self.tab_main = QtWidgets.QWidget()  # 0. Главная вкладка с данными
#         self.tab_settings = QtWidgets.QWidget()  # 1. Настройки
#         # добавляем "0" таб на вкладку табов
#         self.tabs.addTab(self.tab_main, "")  # 0. Главная вкладка с данными
#         self.tabs.setTabIcon(0, draw_ico)
#         self.tabs.setTabToolTip(0, "Главня вкладка")
#         self.tab_main.layout = QtWidgets.QFormLayout(self)
#
#         # Рамка №1 (то что будет в рамке 1)
#         self.scale_name = QtWidgets.QLineEdit()
#         self.scale_name.setPlaceholderText("Масштаб")
#         self.scale_name.setToolTip("[м, пикс.]")
#         self.scale_name.setReadOnly(True)
#
#         # Рамка №2 (то что будет в рамке 2)
#         self.type_act = QtWidgets.QComboBox()  # д. проектируемый/существующий объект
#         self.type_act.addItems(["Объект", "Масштаб", "Расстояние", "Площадь"])
#         self.type_act.setItemIcon(0, object_ico)
#         self.type_act.setItemIcon(1, scale_ico)
#         self.type_act.setItemIcon(2, dist_ico)
#         self.type_act.setItemIcon(3, area_ico)
#         self.result_lbl = QtWidgets.QLabel()
#         self.draw_btn = QtWidgets.QPushButton("Применить")
#         self.draw_btn.setCheckable(True)
#         self.draw_btn.setChecked(False)
#
#         # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
#         # т.к. элементы будут добавляться и их
#         # потом нужно будет объединять в группы
#
#         # Рамка №1
#         layout_scale = QtWidgets.QFormLayout(self)
#         GB_scale = QtWidgets.QGroupBox('Масштаб')
#         GB_scale.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_scale.addRow("", self.scale_name)
#         GB_scale.setLayout(layout_scale)
#         # Рамка №2
#         layout_act = QtWidgets.QFormLayout(self)
#         GB_act = QtWidgets.QGroupBox('Действие')
#         GB_act.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_act.addRow("", self.type_act)
#         layout_act.addRow("", self.draw_btn)
#         layout_act.addRow("", self.result_lbl)
#         GB_act.setLayout(layout_act)
#         # Собираем рамки
#         self.tab_main.layout.addWidget(GB_scale)
#         self.tab_main.layout.addWidget(GB_act)
#         # Размещаем на табе
#         self.tab_main.setLayout(self.tab_main.layout)
#
#         # добавляем "1" таб на вкладку табов
#         self.tabs.addTab(self.tab_settings, "")  # 1. Настройки
#         self.tabs.setTabIcon(1, settings_ico)
#         self.tabs.setTabToolTip(1, "Настройки")
#         self.tab_settings.layout = QtWidgets.QFormLayout(self)
#         # Рамка №1 (то что будет в рамке 1)
#         self.db_name = QtWidgets.QLineEdit()  # Наименование  базы данных
#         self.db_name.setPlaceholderText("Наименование базы данных")
#         self.db_name.setToolTip("Наименование базы данных")
#         self.db_name.setReadOnly(True)
#         # Рамка №2 (то что будет в рамке 2)
#         self.plan_list = QtWidgets.QComboBox()  # ген.планы объекта
#         self.plan_list.addItems(["--Нет ген.планов-- "])
#         self.plan_list.setToolTip("""Ген.планы объекта""")
#         # self.plan_list.activated[str].connect(self.plan_list_select)
#
#         # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
#         # т.к. элементы будут добавляться и их
#         # потом нужно будет объединять в группы
#         # Рамка №1
#         layout_db = QtWidgets.QFormLayout(self)
#         GB_db = QtWidgets.QGroupBox('База данных')
#         GB_db.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_db.addRow("", self.db_name)
#         GB_db.setLayout(layout_db)
#         # Рамка №2
#         layout_plan = QtWidgets.QFormLayout(self)
#         GB_plan = QtWidgets.QGroupBox('Ген.план')
#         GB_plan.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_plan.addRow("", self.plan_list)
#         GB_plan.setLayout(layout_plan)
#         # Размещаем на табе
#         self.tab_settings.layout.addWidget(GB_db)
#         self.tab_settings.layout.addWidget(GB_plan)
#         # Размещаем на табе
#         self.tab_settings.setLayout(self.tab_settings.layout)
#
#         grid.addWidget(self.table, 0, 0, 1, 1)
#         grid.addWidget(self.tabs, 0, 1, 1, 1)
#         central_widget.setLayout(grid)
#         self.setCentralWidget(central_widget)
#
#         # База данных (меню)
#         main_menu = QtWidgets.QMenu('База данных', self)
#         file_is_open = QtWidgets.QAction(ok_ico, 'Подключение', self)
#         file_is_open.setStatusTip('Подключиться к базе данных')
#         file_is_open.triggered.connect(self.file_is_open)
#         main_menu.addAction(file_is_open)
#
#         # Формы добавления информации в БД (меню)
#         add_menu = QtWidgets.QMenu('Добавить в базу данных', self)
#         company_add = QtWidgets.QAction(company_ico, 'Компания', self)
#         company_add.setStatusTip('Добавить новую компанию')
#         company_add.triggered.connect(self.company_add)
#         add_menu.addAction(company_add)
#         opo_add = QtWidgets.QAction(object_ico, 'Опасный производственный объект', self)
#         opo_add.setStatusTip('Добавить новый опасный производственный объект')
#         # opo_add.triggered.connect(self.company_add)
#         add_menu.addAction(opo_add)
#         doc_add = QtWidgets.QAction(doc_ico, 'Документация объекта', self)
#         doc_add.setStatusTip('Добавить документацию опасного производственного объекта')
#         # doc_add.triggered.connect(self.company_add)
#         add_menu.addAction(doc_add)
#         line_obj_add = QtWidgets.QAction(line_ico, 'Линейный объект', self)
#         line_obj_add.setStatusTip('Добавить линейный объект')
#         # doc_add.triggered.connect(self.company_add)
#         add_menu.addAction(line_obj_add)
#         state_obj_add = QtWidgets.QAction(state_ico, 'Стационарный объект', self)
#         state_obj_add.setStatusTip('Добавить новый стационарный объект')
#         # company_add.triggered.connect(self.company_add)
#         add_menu.addAction(state_obj_add)
#         build_obj_add = QtWidgets.QAction(build_ico, 'Здание/сооружение', self)
#         build_obj_add.setStatusTip('Добавить новое здание/сооружение')
#         # company_add.triggered.connect(self.company_add)
#         add_menu.addAction(build_obj_add)
#         project_add = QtWidgets.QAction(project_ico, 'Проект', self)
#         project_add.setStatusTip('Добавить новую проектную документацию')
#         # company_add.triggered.connect(self.company_add)
#         add_menu.addAction(project_add)
#         epb_add = QtWidgets.QAction(project2_ico, 'Документация с ЭПБ', self)
#         epb_add.setStatusTip('Добавить новую документацию c ЭПБ')
#         # company_add.triggered.connect(self.company_add)
#         add_menu.addAction(epb_add)
#
#         # Формы удаления информации из БД (меню)
#         del_menu = QtWidgets.QMenu('Удалить из базы данных', self)
#         company_del = QtWidgets.QAction(company_ico, 'Компания', self)
#         company_del.setStatusTip('Удалить компанию')
#         # company_del.triggered.connect(self.company_del)
#         del_menu.addAction(company_del)
#         opo_del = QtWidgets.QAction(object_ico, 'Опасный производственный объект', self)
#         opo_del.setStatusTip('Добавить новый опасный производственный объект')
#         # opo_del.triggered.connect(self.company_del)
#         del_menu.addAction(opo_del)
#         doc_del = QtWidgets.QAction(doc_ico, 'Документация объекта', self)
#         doc_del.setStatusTip('Добавить документацию опасного производственного объекта')
#         # doc_del.triggered.connect(self.company_del)
#         del_menu.addAction(doc_del)
#         line_obj_del = QtWidgets.QAction(line_ico, 'Линейный объект', self)
#         line_obj_del.setStatusTip('Добавить линейный объект')
#         # doc_del.triggered.connect(self.company_del)
#         del_menu.addAction(line_obj_del)
#         state_obj_del = QtWidgets.QAction(state_ico, 'Стационарный объект', self)
#         state_obj_del.setStatusTip('Добавить новый стационарный объект')
#         # company_del.triggered.connect(self.company_del)
#         del_menu.addAction(state_obj_del)
#         build_obj_del = QtWidgets.QAction(build_ico, 'Здание/сооружение', self)
#         build_obj_del.setStatusTip('Добавить новое здание/сооружение')
#         # company_del.triggered.connect(self.company_del)
#         del_menu.addAction(build_obj_del)
#         project_del = QtWidgets.QAction(project_ico, 'Проект', self)
#         project_del.setStatusTip('Добавить новую проектную документацию')
#         # company_del.triggered.connect(self.company_del)
#         del_menu.addAction(project_del)
#         epb_del = QtWidgets.QAction(project2_ico, 'Документация с ЭПБ', self)
#         epb_del.setStatusTip('Добавить новую документацию c ЭПБ')
#         # company_del.triggered.connect(self.company_del)
#         del_menu.addAction(epb_del)
#
#         # Выход из приложения
#         exit_prog = QtWidgets.QAction(exit_ico, 'Выход', self)
#         exit_prog.setShortcut('Ctrl+Q')
#         exit_prog.setStatusTip('Выход из Storage_app')
#         exit_prog.triggered.connect(self.close_event)
#
#         # Справка
#         help_show = QtWidgets.QAction(question_ico, 'Справка', self)
#         help_show.setShortcut('F1')
#         help_show.setStatusTip('Открыть справку Storage_app')
#         help_show.triggered.connect(self.help_show)
#
#         # О приложении
#         about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
#         about_prog.setShortcut('F2')
#         about_prog.setStatusTip('О приложении Storage_app')
#         about_prog.triggered.connect(self.about_programm)
#
#         # Меню приложения (верхняя плашка)
#         menubar = self.menuBar()
#         file_menu = menubar.addMenu('Файл')
#         file_menu.addMenu(main_menu)
#         file_menu.addAction(exit_prog)
#         db_menu = menubar.addMenu('База данных')
#         db_menu.addMenu(add_menu)
#         db_menu.addMenu(del_menu)
#         help_menu = menubar.addMenu('Справка')
#         help_menu.addAction(help_show)
#         help_menu.addAction(about_prog)
#         # Установить статусбар
#         self.statusBar()
#
#         # toolbar = self.addToolBar('Выход')
#         # toolbar.addAction(exitAction)
#
#         if not parent:
#             self.show()
#
#     # 1. Вкладка ФАЙЛ
#     def file_is_open(self):
#         messageBox = QtWidgets.QMessageBox(
#             QtWidgets.QMessageBox.Question,
#             "Соединение с базой данных",
#             "Соединение с базой данных проверяется"
#             "только для серверных баз данных",
#             (QtWidgets.QMessageBox.Ok)
#         )
#         messageBox.setWindowIcon(self.main_ico)
#         resultCode = messageBox.exec_()
#         if resultCode == QtWidgets.QMessageBox.Ok:
#             return
#
#     #     Функция выхода из программы
#     def close_event(self) -> None:
#         messageBox = QtWidgets.QMessageBox(
#             QtWidgets.QMessageBox.Question,
#             "Выход из программы",
#             "Выйти из программы?",
#             (QtWidgets.QMessageBox.Yes
#              | QtWidgets.QMessageBox.No)
#         )
#         messageBox.setButtonText(QtWidgets.QMessageBox.Yes, "Да")
#         messageBox.setButtonText(QtWidgets.QMessageBox.No, "Нет")
#         messageBox.setWindowIcon(self.main_ico)
#         resultCode = messageBox.exec_()
#         if resultCode == QtWidgets.QMessageBox.No:
#             return
#         elif resultCode == QtWidgets.QMessageBox.Yes:
#             return self.close()
#
#
#     # 2. База данных
#     def company_add(self):
#         print("company_add")
#         self.dialog_company_add.show()
#
#     def plan_replace(self):
#         print("plan_replace")
#
#     def plan_save(self):
#         print("plan_save")
#
#     def plan_clear(self):
#         print("plan_clear")
#
#     def plan_del(self):
#         print("plan_del")
#
#
#
#     # 2. Вкладка СПРАВКА
#     # функция справки
#     def help_show(self):
#         print("help_show")
#
#     #     Функция "О программе"
#     def about_programm(self) -> None:
#         messageBox = QtWidgets.QMessageBox(
#             QtWidgets.QMessageBox.Information,
#             "О программе",
#             """Программа <b>Storage_app</b>. Предназначена для хранения данных об опасных производственных объектах.
# Разрабочик: <b>npfgsk.ru</b>""",
#             (QtWidgets.QMessageBox.Ok)
#         )
#         messageBox.setWindowIcon(self.main_ico)
#         messageBox.exec_()
#
#     # ОБЩИЕ ФУНКЦИИ
#     def convertToBinaryData(self, file_path):
#         # Конвертирование в BLOB
#         with open(file_path, 'rb') as file:
#             blobData = file.read()
#         return blobData
#
# class Company_add(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()
#         self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
#         folder_file_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/folder_file.png')
#         self.setWindowTitle('Данные о компании')
#         self.setWindowIcon(self.main_ico)
#         #  Создаем валидаторы для полей ввода
#         onlyInt = QtGui.QIntValidator()  # only int
#         # Рамка №1 (то что будет в рамке 1)
#         self.name_company = QtWidgets.QLineEdit()
#         self.name_company.setPlaceholderText("Наименование компании")
#         self.full_name_manager = QtWidgets.QLineEdit()
#         self.full_name_manager.setPlaceholderText("Ф.И.О. руководителя")
#         self.ur_address = QtWidgets.QLineEdit()
#         self.ur_address.setPlaceholderText("Юридический адрес")
#         self.post_address = QtWidgets.QLineEdit()
#         self.post_address.setPlaceholderText("Почтовый адрес")
#         self.telephone = QtWidgets.QLineEdit()
#         self.telephone.setPlaceholderText("Телефон")
#         self.telephone.setValidator(onlyInt)
#         self.fax = QtWidgets.QLineEdit()
#         self.fax.setPlaceholderText("Факс")
#         self.fax.setValidator(onlyInt)
#         self.inn_number = QtWidgets.QLineEdit()
#         self.inn_number.setPlaceholderText("ИНН")
#         self.inn_number.setValidator(onlyInt)
#         self.kpp_number = QtWidgets.QLineEdit()
#         self.kpp_number.setPlaceholderText("КПП")
#         self.kpp_number.setValidator(onlyInt)
#         self.ogrn_number = QtWidgets.QLineEdit()
#         self.ogrn_number.setPlaceholderText("ОГРН")
#         self.ogrn_number.setValidator(onlyInt)
#
#         self.license_opo = QtWidgets.QLineEdit()
#         self.license_opo.setPlaceholderText("Лицензия (выберете файл)")
#         self.license_opo.setReadOnly(True)
#         license_opo_btn = QtWidgets.QPushButton("")
#         license_opo_btn.setIcon(folder_file_ico)
#         license_opo_btn.clicked.connect(self.folder_file_license)
#         hbox_license_opo = QtWidgets.QHBoxLayout()
#         hbox_license_opo.addWidget(self.license_opo)
#         hbox_license_opo.addWidget(license_opo_btn)
#
#         self.reg_opo = QtWidgets.QLineEdit()
#         self.reg_opo.setPlaceholderText("Регистрация ОПО (выберете файл)")
#         self.reg_opo.setReadOnly(True)
#         reg_opo_btn = QtWidgets.QPushButton("")
#         reg_opo_btn.setIcon(folder_file_ico)
#         reg_opo_btn.clicked.connect(self.folder_file_reg)
#         hbox_reg_opo = QtWidgets.QHBoxLayout()
#         hbox_reg_opo.addWidget(self.reg_opo)
#         hbox_reg_opo.addWidget(reg_opo_btn)
#
#         self.position_pk = QtWidgets.QLineEdit()
#         self.position_pk.setPlaceholderText("Положение о ПК (выберете файл)")
#         self.position_pk.setReadOnly(True)
#         position_pk_btn = QtWidgets.QPushButton("")
#         position_pk_btn.setIcon(folder_file_ico)
#         position_pk_btn.clicked.connect(self.folder_file_pk)
#         hbox_position_pk = QtWidgets.QHBoxLayout()
#         hbox_position_pk.addWidget(self.position_pk)
#         hbox_position_pk.addWidget(position_pk_btn)
#
#         self.position_crash = QtWidgets.QLineEdit()
#         self.position_crash.setPlaceholderText("Положение об инцендентах (выберете файл)")
#         self.position_crash.setReadOnly(True)
#         position_crash_btn = QtWidgets.QPushButton("")
#         position_crash_btn.setIcon(folder_file_ico)
#         position_crash_btn.clicked.connect(self.folder_file_crash)
#         hbox_position_crash = QtWidgets.QHBoxLayout()
#         hbox_position_crash.addWidget(self.position_crash)
#         hbox_position_crash.addWidget(position_crash_btn)
#         # Рамка №2 (то что будет в рамке 2)
#         save_in_db_btn = QtWidgets.QPushButton("Записать в базу данных")
#         save_in_db_btn.clicked.connect(self.write_in_db)
#
#         # Упаковываем все  (делаем все в QGroupBox
#         # т.к. элементы будут добавляться и их
#         # потом нужно будет объединять в группы
#         # Рамка №1
#         layout_info = QtWidgets.QFormLayout(self)
#         GB_info = QtWidgets.QGroupBox('Данные о компании добавляемые в базу данных')
#         GB_info.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_info.addRow("1. ", self.name_company)
#         layout_info.addRow("2. ", self.full_name_manager)
#         layout_info.addRow("3. ", self.ur_address)
#         layout_info.addRow("4. ", self.post_address)
#         layout_info.addRow("5. ", self.telephone)
#         layout_info.addRow("6. ", self.fax)
#         layout_info.addRow("7. ", self.inn_number)
#         layout_info.addRow("8. ", self.kpp_number)
#         layout_info.addRow("9. ", self.ogrn_number)
#         layout_info.addRow("10. ", hbox_license_opo)
#         layout_info.addRow("11. ", hbox_reg_opo)
#         layout_info.addRow("12. ", hbox_position_pk)
#         layout_info.addRow("13. ", hbox_position_crash)
#
#         GB_info.setLayout(layout_info)
#         # Рамка №2
#         layout_btn = QtWidgets.QFormLayout(self)
#         GB_btn = QtWidgets.QGroupBox('Действие')
#         GB_btn.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_btn.addRow("", save_in_db_btn)
#         GB_btn.setLayout(layout_btn)
#
#         vbox = QtWidgets.QVBoxLayout()
#         vbox.addWidget(GB_info)
#         vbox.addWidget(GB_btn)
#         self.setLayout(vbox)
#
#     def folder_file_license(self):
#         path = QtWidgets.QFileDialog.getOpenFileName(self, 'Файл лицензии', "/home", ("PDF (*.pdf)"))[0]
#         self.license_opo.setText(path)
#
#     def folder_file_reg(self):
#         path = QtWidgets.QFileDialog.getOpenFileName(self, 'Файл свидетельства орегистрации',
#                                                      "/home", ("PDF (*.pdf)"))[0]
#         self.reg_opo.setText(path)
#
#     def folder_file_pk(self):
#         path = QtWidgets.QFileDialog.getOpenFileName(self, 'Файл положения о ПК', "/home", ("PDF (*.pdf)"))[0]
#         self.position_pk.setText(path)
#
#
#     def folder_file_crash(self):
#         path = QtWidgets.QFileDialog.getOpenFileName(self, 'Файл положения о инцендентах', "/home", ("PDF (*.pdf)"))[0]
#         self.position_crash.setText(path)
#
#     def write_in_db(self):
#         print("Start write in DB")
#         check = self.check_data()
#         if check:
#             print("Идем дальше данные введены")
#
#         else:
#             messageBox = QtWidgets.QMessageBox(
#                 QtWidgets.QMessageBox.Warning,
#                 "Запись данных",
#                 """Запись не выполненна!""",
#                 (QtWidgets.QMessageBox.Ok)
#             )
#             messageBox.setWindowIcon(self.main_ico)
#             messageBox.exec_()
#
#     def check_data(self):
#         data = (
#             self.name_company.text(),
#             self.full_name_manager.text(),
#             self.ur_address.text(),
#             self.post_address.text(),
#             self.telephone.text(),
#             self.fax.text(),
#             self.inn_number.text(),
#             self.kpp_number.text(),
#             self.ogrn_number.text(),
#             self.license_opo.text(),
#             self.reg_opo.text(),
#             self.position_pk.text(),
#             self.position_crash.text()
#         )
#
#         for i in data:
#             if i == '':
#                 messageBox = QtWidgets.QMessageBox(
#                     QtWidgets.QMessageBox.Warning,
#                     "Проверка данных",
#                     """Данные введены не верно. Проверьте заполнение!""",
#                     (QtWidgets.QMessageBox.Ok)
#                 )
#                 messageBox.setWindowIcon(self.main_ico)
#                 messageBox.exec_()
#                 return False
#         return True
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     ex = Storage_app()
#     app.exec_()