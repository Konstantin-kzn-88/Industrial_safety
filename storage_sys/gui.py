# -----------------------------------------------------------
# Графический интерфейс предназначен для взаимодействия с БД
# объектов для ОПО нефтедобычи
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from pathlib import Path

from PySide2 import QtSql, QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtSql import QSqlRelationalTableModel


class Relational_table_model_with_icon(QSqlRelationalTableModel):
    def __init__(self, table_state="company", **kwargs):
        self.table_state = table_state
        QSqlRelationalTableModel.__init__(self, **kwargs)

    def data(self, index, role=Qt.DisplayRole):
        icon = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
        if self.table_state == "company":
            if index.column() == 11 and role == Qt.DisplayRole:
                return ""
            if index.column() == 11 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 12 and role == Qt.DisplayRole:
                return ""
            if index.column() == 12 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 13 and role == Qt.DisplayRole:
                return ""
            if index.column() == 13 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 14 and role == Qt.DisplayRole:
                return ""
            if index.column() == 14 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
        else:
            if index.column() == 2 and role == Qt.DisplayRole:  # для второго столбца, скроем выводимый текст
                return ""
            if index.column() == 2 and role == Qt.DecorationRole:  # и для него же выведем иконку в качестве декора
                return QtGui.QIcon('info.png')
        return QSqlRelationalTableModel.data(self, index,
                                             role)  # все остальное должно штатно обработаться qsqltablemodel


class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.tst_var = "company"
        self.createConnection()
        self.fillTable()  # !!! тестовое заполнение базы данных
        self.createModel()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.initUI()


        # layout = QtWidgets.QVBoxLayout(self.centralWidget)
        # layout.addWidget(self.view)

        if not parent:
            self.show()

    def createConnection(self):
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
                "class_opo TEXT NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO opo (id, id_company, name_opo, "
                      "address_opo, reg_number_opo, class_opo)"
                      "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo)")

        query.bindValue(":id", 1)
        query.bindValue(":id_company", 1)
        query.bindValue(":name_opo", 'Фонд скважин Муслюмовского месторождения нефти и газа')
        query.bindValue(":address_opo", 'РФ, РТ, Муслюмовский, Азнакаевский и Сармановский районы')
        query.bindValue(":reg_number_opo", 'А43-01341-0005')
        query.bindValue(":class_opo", '3')
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO opo (id, id_company, name_opo, "
                      "address_opo, reg_number_opo, class_opo)"
                      "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo)")

        query.bindValue(":id", 2)
        query.bindValue(":id_company", 2)
        query.bindValue(":name_opo", 'Фонд скважин Урмышлинского месторождения нефти')
        query.bindValue(":address_opo", 'РФ, РТ, Черемшанский район, Лениногорский районы')
        query.bindValue(":reg_number_opo", 'А43-01109-0001')
        query.bindValue(":class_opo", '3')
        query.exec_()

        #                             vvvvvvvvvvvvv
        q.exec_("DROP TABLE IF EXISTS documentation;")
        q.exec_("CREATE TABLE documentation ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "type_doc TEXT NOT NULL, "
                "reg_doc TEXT NOT NULL, "
                "date_doc TEXT NOT NULL, "
                "doc BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO documentation (id, id_opo, type_doc, reg_doc, date_doc, doc)"
                      "VALUES (:id, :id_opo, :type_doc, :reg_doc,:date_doc, :doc)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":type_doc", 'Декларция промышленной безопасности')
        query.bindValue(":reg_doc", '43-ДПБ-00001-01')
        query.bindValue(":date_doc", '14-12-2018')
        query.bindValue(":doc", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO documentation (id, id_opo, type_doc, reg_doc, date_doc, doc)"
                      "VALUES (:id, :id_opo, :type_doc, :reg_doc,:date_doc, :doc)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":type_doc", 'Консервация насоса Н-1')
        query.bindValue(":reg_doc", '43-ЭПБ-00003-05')
        query.bindValue(":date_doc", '25-07-2021')
        query.bindValue(":doc", test_BLOB)
        query.exec_()

        #                             vvvvvvvv
        q.exec_("DROP TABLE IF EXISTS line_obj;")
        q.exec_("CREATE TABLE line_obj ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "reg_number INT NOT NULL, "
                "name_obj TEXT NOT NULL, "
                "substance TEXT NOT NULL, "
                "lenght DECIMAL NOT NULL, "
                "diameter DECIMAL NOT NULL, "
                "pressure DECIMAL NOT NULL, "
                "status TEXT NOT NULL, "
                "date_manufacture TEXT NOT NULL, "
                "date_entry TEXT NOT NULL, "
                "date_upto TEXT NOT NULL, "
                "passport BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO line_obj (id, id_opo, reg_number, name_obj, substance, lenght,"
                      "diameter, pressure, status, date_manufacture, date_entry, date_upto, passport)"
                      "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :lenght,"
                      ":diameter, :pressure, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":reg_number", '1258')
        query.bindValue(":name_obj", 'Трубопровод')
        query.bindValue(":substance", 'нефть')
        query.bindValue(":lenght", 1.225)
        query.bindValue(":diameter", 229)
        query.bindValue(":pressure", 0.23)
        query.bindValue(":status", 'Действующий')
        query.bindValue(":date_manufacture", '01-01-1988')
        query.bindValue(":date_entry", '01-05-1988')
        query.bindValue(":date_upto", '01-01-2020')
        query.bindValue(":passport", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO line_obj (id, id_opo, reg_number, name_obj, substance, lenght,"
                      "diameter, pressure, status, date_manufacture, date_entry, date_upto, passport)"
                      "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :lenght,"
                      ":diameter, :pressure, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":reg_number", '1347')
        query.bindValue(":name_obj", 'Трубопровод')
        query.bindValue(":substance", 'нефтяная эмульсия')
        query.bindValue(":lenght", 5.03)
        query.bindValue(":diameter", 114)
        query.bindValue(":pressure", 0.56)
        query.bindValue(":status", 'Законсервирован')
        query.bindValue(":date_manufacture", '01-01-1995')
        query.bindValue(":date_entry", '01-05-1996')
        query.bindValue(":date_upto", '01-01-2025')
        query.bindValue(":passport", test_BLOB)
        query.exec_()

        #                             vvvvvvvvv
        q.exec_("DROP TABLE IF EXISTS state_obj;")
        q.exec_("CREATE TABLE state_obj ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "reg_number INT NOT NULL, "
                "name_obj TEXT NOT NULL, "
                "substance TEXT NOT NULL, "
                "volume DECIMAL NOT NULL, "
                "temperature DECIMAL NOT NULL, "
                "pressure DECIMAL NOT NULL, "
                "alpha DECIMAL NOT NULL, "
                "status TEXT NOT NULL, "
                "date_manufacture TEXT NOT NULL, "
                "date_entry TEXT NOT NULL, "
                "date_upto TEXT NOT NULL, "
                "passport BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO state_obj (id, id_opo, reg_number, name_obj, substance, volume,"
                      "temperature, pressure, alpha, status, date_manufacture, date_entry, date_upto, passport)"
                      "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :volume,"
                      ":temperature, :pressure, :alpha, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":reg_number", '12589')
        query.bindValue(":name_obj", 'Емкость Е-1')
        query.bindValue(":substance", 'нефть')
        query.bindValue(":volume", 200)
        query.bindValue(":temperature", 55)
        query.bindValue(":pressure", 0.23)
        query.bindValue(":alpha", 0.25)
        query.bindValue(":status", 'Действующий')
        query.bindValue(":date_manufacture", '01-01-1988')
        query.bindValue(":date_entry", '01-05-1988')
        query.bindValue(":date_upto", '01-01-2020')
        query.bindValue(":passport", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO state_obj (id, id_opo, reg_number, name_obj, substance, volume,"
                      "temperature, pressure, alpha, status, date_manufacture, date_entry, date_upto, passport)"
                      "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :volume,"
                      ":temperature, :pressure, :alpha, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":reg_number", '2589')
        query.bindValue(":name_obj", 'Нефтесепаратор НГС-2')
        query.bindValue(":substance", 'нефть')
        query.bindValue(":volume", 100)
        query.bindValue(":temperature", 55)
        query.bindValue(":pressure", 0.23)
        query.bindValue(":alpha", 0.25)
        query.bindValue(":status", 'Действующий')
        query.bindValue(":date_manufacture", '01-01-2005')
        query.bindValue(":date_entry", '01-05-2006')
        query.bindValue(":date_upto", '01-01-2027')
        query.bindValue(":passport", test_BLOB)
        query.exec_()

        #                             vvvvvvvvvv
        q.exec_("DROP TABLE IF EXISTS build_obj;")
        q.exec_("CREATE TABLE build_obj ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "name_obj TEXT NOT NULL, "
                "status TEXT NOT NULL, "
                "date_manufacture TEXT NOT NULL, "
                "date_entry TEXT NOT NULL, "
                "date_upto TEXT NOT NULL, "
                "doc BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO build_obj (id, id_opo, name_obj, status, "
                      "date_manufacture, date_entry, date_upto, doc)"
                      "VALUES (:id, :id_opo, :name_obj, :status, :date_manufacture, :date_entry, "
                      ":date_upto, :doc)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":name_obj", 'Операторная')
        query.bindValue(":status", 'Консервация')
        query.bindValue(":date_manufacture", '14-12-2018')
        query.bindValue(":date_entry", '14-12-2018')
        query.bindValue(":date_upto", '14-12-2028')
        query.bindValue(":doc", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO build_obj (id, id_opo, name_obj, status, "
                      "date_manufacture, date_entry, date_upto, doc)"
                      "VALUES (:id, :id_opo, :name_obj, :status, :date_manufacture, :date_entry, "
                      ":date_upto, :doc)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":name_obj", 'Лаборатория')
        query.bindValue(":status", 'Дествующая')
        query.bindValue(":date_manufacture", '14-12-2010')
        query.bindValue(":date_entry", '14-12-2013')
        query.bindValue(":date_upto", '14-12-2038')
        query.bindValue(":doc", test_BLOB)
        query.exec_()

        #                             vvvvvvv
        q.exec_("DROP TABLE IF EXISTS project;")
        q.exec_("CREATE TABLE project ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "name_project TEXT NOT NULL, "
                "date_project TEXT NOT NULL, "
                "pz_project BLOB NOT NULL, "
                "pzu_project BLOB NOT NULL, "
                "kr_project BLOB NOT NULL, "
                "ios_project BLOB NOT NULL, "
                "pos_project BLOB NOT NULL, "
                "another_project BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO project (id, id_opo, name_project, date_project, "
                      "pz_project, pzu_project, kr_project, ios_project,"
                      "pos_project, another_project)"
                      "VALUES (:id, :id_opo, :name_project, :date_project, :pz_project, :pzu_project, "
                      ":kr_project, :ios_project, :pos_project, :another_project)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":name_project", 'Обустройство кустов скважин')
        query.bindValue(":date_project", '14-12-2018')
        query.bindValue(":pz_project", test_BLOB)
        query.bindValue(":pzu_project", test_BLOB)
        query.bindValue(":kr_project", test_BLOB)
        query.bindValue(":ios_project", test_BLOB)
        query.bindValue(":pos_project", test_BLOB)
        query.bindValue(":another_project", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO project (id, id_opo, name_project, date_project, "
                      "pz_project, pzu_project, kr_project, ios_project,"
                      "pos_project, another_project)"
                      "VALUES (:id, :id_opo, :name_project, :date_project, :pz_project, :pzu_project, "
                      ":kr_project, :ios_project, :pos_project, :another_project)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":name_project", 'Обустройство куста скважин')
        query.bindValue(":date_project", '14-12-2015')
        query.bindValue(":pz_project", test_BLOB)
        query.bindValue(":pzu_project", test_BLOB)
        query.bindValue(":kr_project", test_BLOB)
        query.bindValue(":ios_project", test_BLOB)
        query.bindValue(":pos_project", test_BLOB)
        query.bindValue(":another_project", test_BLOB)
        query.exec_()

        #                             vvv
        q.exec_("DROP TABLE IF EXISTS epb;")
        q.exec_("CREATE TABLE epb ("
                "id INT PRIMARY KEY, "
                "id_opo INT NOT NULL, "
                "name_doc TEXT NOT NULL, "
                "date_doc TEXT NOT NULL, "
                "epb_doc BLOB NOT NULL );")

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO epb (id, id_opo, name_doc, date_doc, epb_doc)"
                      "VALUES (:id, :id_opo, :name_doc, :date_doc, :epb_doc)")

        query.bindValue(":id", 1)
        query.bindValue(":id_opo", 1)
        query.bindValue(":name_doc", 'ЭПБ на задвижку')
        query.bindValue(":date_doc", '14-12-2018')
        query.bindValue(":epb_doc", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO epb (id, id_opo, name_doc, date_doc, epb_doc)"
                      "VALUES (:id, :id_opo, :name_doc, :date_doc, :epb_doc)")

        query.bindValue(":id", 2)
        query.bindValue(":id_opo", 2)
        query.bindValue(":name_doc", 'ЭПБ на трубу')
        query.bindValue(":date_doc", '14-12-2018')
        query.bindValue(":epb_doc", test_BLOB)
        query.exec_()

        self.db.commit()

    def createModel(self):
        """
        Создание модели для отображения
        """
        self.model = Relational_table_model_with_icon(db=self.db, table_state = self.tst_var)
        self.model.setTable("company")
        # self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        # self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наиманование")
        # self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Документы")
        self.model.select()

    def initUI(self):
        # Иконки
        self.table_state = "company"
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        company_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/company.png')
        state_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/state.png')
        ok_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/ok.png')
        object_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/object.png')
        doc_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/document.png')
        line_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/tube.png')
        build_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/build.png')
        project_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/project.png')
        project2_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/project2.png')
        exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
        info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
        question_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/question.png')
        # ВИД
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        mode = QtWidgets.QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)
        # выравнивание по содержимому
        self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.view.horizontalHeader().setMinimumSectionSize(0)
        # запрет на редактирование
        self.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # Главное окно
        self.setGeometry(500, 500, 950, 750)
        self.setWindowTitle('Storage_app')
        self.setWindowIcon(self.main_ico)
        # UI
        grid = QtWidgets.QGridLayout(self)
        grid.setColumnStretch(0, 6)
        grid.setColumnStretch(1, 2)
        # т.к. данных  много создадим
        # вкладки табов
        self.tabs = QtWidgets.QTabWidget()  # создаем вкладки табов
        self.tab_main = QtWidgets.QWidget()  # 0. Главная вкладка
        self.tab_settings = QtWidgets.QWidget()  # 1. Настройки
        # добавляем "0" таб на вкладку табов
        self.tabs.addTab(self.tab_main, "")  # 0. Главная вкладка с данными
        self.tabs.setTabIcon(0, self.main_ico)
        self.tabs.setTabToolTip(0, "Главня вкладка")
        self.tab_main.layout = QtWidgets.QFormLayout(self)
        # то что будет во вкладке 0
        self.table_box = QtWidgets.QComboBox()  # возможные таблицы из БД
        self.table_box.addItems(["Компании", "ОПО", "Документация ОПО", "Линейные объекты", "Стационарные объекты",
                                 "Здания и сооружения", "Проекты", "Экспертизы пром.безопасности"])
        self.table_box.setItemIcon(0, company_ico)
        self.table_box.setItemIcon(1, object_ico)
        self.table_box.setItemIcon(2, doc_ico)
        self.table_box.setItemIcon(3, line_ico)
        self.table_box.setItemIcon(4, state_ico)
        self.table_box.setItemIcon(5, build_ico)
        self.table_box.setItemIcon(6, project_ico)
        self.table_box.setItemIcon(7, project2_ico)
        self.table_box.setToolTip("""Таблицы базы данных""")
        # self.table_box.activated[str].connect(self.table_select)

        # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
        # т.к. элементы будут добавляться и их
        # потом нужно будет объединять в группы

        # Рамка №0
        layout_table_select = QtWidgets.QFormLayout(self)
        GB_table_select = QtWidgets.QGroupBox('Таблицы базы данных')
        GB_table_select.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_table_select.addRow("", self.table_box)
        GB_table_select.setLayout(layout_table_select)
        # Собираем рамки
        self.tab_main.layout.addWidget(GB_table_select)
        # Размещаем на табе
        self.tab_main.setLayout(self.tab_main.layout)
        # Размещаем на сетке
        grid.addWidget(self.view, 0, 0, 1, 1)
        grid.addWidget(self.tabs, 0, 1, 1, 1)
        self.centralWidget.setLayout(grid)
        self.setCentralWidget(self.centralWidget)


    def closeEvent(self, event):
        if (self.db.open()):
            self.db.close()

    def convertToBinaryData(self, file_path):
        # Конвертирование в BLOB
        with open(file_path, 'rb') as file:
            blobData = file.read()
        return blobData


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    w = Storage_app()
    app.exec_()


#
# class Storage_app(QtWidgets.QMainWindow):
#     """
#     Основной класс базы данных реализующий представление
#     базы данных ОПО
#     """
#
#     def __init__(self, parent=None) -> None:
#         super().__init__()
#
#         # Иконки
#         self.table_state = "company"
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
#         exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
#         info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
#         question_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/question.png')
#
#         # Главное окно
#         self.setGeometry(500, 500, 950, 750)
#         self.setWindowTitle('Storage_app')
#         self.setWindowIcon(self.main_ico)
#         # !!! тестовое заполнение базы данных   #
#         # self.fillTable()                      #
#         self.createConnection()  # создание подключения к БД
#         self.createModel(table_state=self.table_state)  # создание модели
#         # Вид модели
#         self.view = QtWidgets.QTableView()
#         self.view.setModel(self.model)
#         mode = QtWidgets.QAbstractItemView.SingleSelection
#         self.view.setSelectionMode(mode)
#         # выравнивание по содержимому
#         self.view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
#         self.view.horizontalHeader().setMinimumSectionSize(0)
#         # запрет на редактирование
#         self.view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
#
#         self.centralWidget = QtWidgets.QWidget()
#         self.setCentralWidget(self.centralWidget)  # установим центральный виждет как QWidget
#
#         # UI
#         grid = QtWidgets.QGridLayout(self)
#         grid.setColumnStretch(0, 6)
#         grid.setColumnStretch(1, 2)
#
#         # т.к. данных  много создадим
#         # вкладки табов
#         self.tabs = QtWidgets.QTabWidget()  # создаем вкладки табов
#         self.tab_main = QtWidgets.QWidget()  # 0. Главная вкладка
#         self.tab_settings = QtWidgets.QWidget()  # 1. Настройки
#         # добавляем "0" таб на вкладку табов
#         self.tabs.addTab(self.tab_main, "")  # 0. Главная вкладка с данными
#         self.tabs.setTabIcon(0, self.main_ico)
#         self.tabs.setTabToolTip(0, "Главня вкладка")
#         self.tab_main.layout = QtWidgets.QFormLayout(self)
#         # то что будет во вкладке 0
#         self.table_box = QtWidgets.QComboBox()  # возможные таблицы из БД
#         self.table_box.addItems(["Компании", "ОПО", "Документация ОПО", "Линейные объекты", "Стационарные объекты",
#                                  "Здания и сооружения", "Проекты", "Экспертизы пром.безопасности"])
#         self.table_box.setItemIcon(0, company_ico)
#         self.table_box.setItemIcon(1, object_ico)
#         self.table_box.setItemIcon(2, doc_ico)
#         self.table_box.setItemIcon(3, line_ico)
#         self.table_box.setItemIcon(4, state_ico)
#         self.table_box.setItemIcon(5, build_ico)
#         self.table_box.setItemIcon(6, project_ico)
#         self.table_box.setItemIcon(7, project2_ico)
#         self.table_box.setToolTip("""Таблицы базы данных""")
#         self.table_box.activated[str].connect(self.table_select)
#
#         # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
#         # т.к. элементы будут добавляться и их
#         # потом нужно будет объединять в группы
#
#         # Рамка №0
#         layout_table_select = QtWidgets.QFormLayout(self)
#         GB_table_select = QtWidgets.QGroupBox('Таблицы базы данных')
#         GB_table_select.setStyleSheet("QGroupBox { font-weight : bold; }")
#         layout_table_select.addRow("", self.table_box)
#         GB_table_select.setLayout(layout_table_select)
#         # Собираем рамки
#         self.tab_main.layout.addWidget(GB_table_select)
#         # Размещаем на табе
#         self.tab_main.setLayout(self.tab_main.layout)
#         # Размещаем на сетке
#         grid.addWidget(self.view, 0, 0, 1, 1)
#         grid.addWidget(self.tabs, 0, 1, 1, 1)
#         self.centralWidget.setLayout(grid)
#         self.setCentralWidget(self.centralWidget)
#
#         # МЕНЮ
#         # База данных (меню)
#         main_menu = QtWidgets.QMenu('База данных', self)
#         file_is_open = QtWidgets.QAction(ok_ico, 'Подключение', self)
#         file_is_open.setStatusTip('Подключиться к базе данных')
#         # file_is_open.triggered.connect(self.file_is_open)
#         main_menu.addAction(file_is_open)
#
#         # Формы добавления информации в БД (меню)
#         add_menu = QtWidgets.QMenu('Добавить в базу данных', self)
#         company_add = QtWidgets.QAction(company_ico, 'Компания', self)
#         company_add.setStatusTip('Добавить новую компанию')
#         # company_add.triggered.connect(self.company_add)
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
#         exit_prog.triggered.connect(self.closeEvent)
#
#         # Справка
#         help_show = QtWidgets.QAction(question_ico, 'Справка', self)
#         help_show.setShortcut('F1')
#         help_show.setStatusTip('Открыть справку Storage_app')
#         # help_show.triggered.connect(self.help_show)
#
#         # О приложении
#         about_prog = QtWidgets.QAction(info_ico, 'О приложении', self)
#         about_prog.setShortcut('F2')
#         about_prog.setStatusTip('О приложении Storage_app')
#         # about_prog.triggered.connect(self.about_programm)
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
#
#
#         if not parent:
#             self.show()
#
#     def createConnection(self):
#         """
#         Проверка подключения к базе данных,
#         1) если ее нет, то она создается
#         2) если невозможно подключиться, то пишет в терминале
#         "Cannot establish a database connection"
#         """
#         self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
#         self.db.setDatabaseName("local_base.db")  # !!! .db
#         if not self.db.open():
#             print("Cannot establish a database connection")
#             return False
#
#     def fillTable(self):
#         """
#         Вспомогательная функция заполнениия базы данных
#         Отключить после тестового запуска
#         """
#         file_path = (f"{os.getcwd()}\\test_BLOB.jpg")
#         test_BLOB = self.convertToBinaryData(file_path)
#         test_BLOB = QtCore.QByteArray(test_BLOB)
#
#         self.db.transaction()
#         q = QtSql.QSqlQuery()
#         #
#         q.exec_("DROP TABLE IF EXISTS company;")
#         q.exec_("CREATE TABLE company ("
#                 "id INT PRIMARY KEY, "
#                 "name_company TEXT NOT NULL, "
#                 "full_name_manager TEXT NOT NULL, "
#                 "ur_address TEXT NOT NULL, "
#                 "post_address TEXT NOT NULL, "
#                 "telephone TEXT NOT NULL, "
#                 "email TEXT NOT NULL, "
#                 "fax TEXT DECIMAL NULL, "
#                 "inn_number INT NOT NULL, "
#                 "kpp_number INT NOT NULL, "
#                 "ogrn_number INT NOT NULL, "
#                 "license_opo BLOB NOT NULL, "
#                 "reg_opo BLOB NOT NULL, "
#                 "position_pk BLOB NOT NULL, "
#                 "position_crash BLOB NOT NULL );")
#
#         # Вставка тестовых значений
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO company (id, name_company, full_name_manager, "
#                       "ur_address, post_address, telephone, email, fax, inn_number, kpp_number, ogrn_number, "
#                       "license_opo, reg_opo, position_pk, position_crash) "
#                       "VALUES (:id, :name_company, :full_name_manager, :ur_address,:post_address, :telephone, :email, "
#                       ":fax, :inn_number, :kpp_number, :ogrn_number, :license_opo, :reg_opo, :position_pk, :position_crash)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":name_company", 'АО МЕЛЛЯНЕФТЬ')
#         query.bindValue(":full_name_manager", 'Тазиев Марат Миргазиянович')
#         query.bindValue(":ur_address", 'РФ, РТ, г. Альметьевск, пр-кт Строителей, д. 51')
#         query.bindValue(":post_address", 'РФ, РТ, г. Альметьевск, пр-кт Строителей, д. 51')
#         query.bindValue(":email", 'mellyaneft@tatais.ru')
#         query.bindValue(":telephone", '8 (855) 337-22-60')
#         query.bindValue(":fax", '8 (855) 337-22-61')
#         query.bindValue(":inn_number", 1636002647)
#         query.bindValue(":kpp_number", 164401001)
#         query.bindValue(":ogrn_number", 1021605555179)
#         query.bindValue(":license_opo", test_BLOB)
#         query.bindValue(":reg_opo", test_BLOB)
#         query.bindValue(":position_pk", test_BLOB)
#         query.bindValue(":position_crash", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO company (id, name_company, full_name_manager, "
#                       "ur_address, post_address, telephone, email, fax, inn_number, kpp_number, ogrn_number, "
#                       "license_opo, reg_opo, position_pk, position_crash) "
#                       "VALUES (:id, :name_company, :full_name_manager, :ur_address,:post_address, :telephone, :email, "
#                       ":fax, :inn_number, :kpp_number, :ogrn_number, :license_opo, :reg_opo, :position_pk, :position_crash)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":name_company", 'АО ТАТОЙЛГАЗ')
#         query.bindValue(":full_name_manager", 'Фассахов Роберт Харрасович')
#         query.bindValue(":ur_address", 'РФ, РТ, г. Альметьевск, ул. Тухватуллина, 2а')
#         query.bindValue(":post_address", 'РФ, РТ, г. Альметьевск, ул. Тухватуллина, 2а')
#         query.bindValue(":email", 'reception@tatoilgas.ru')
#         query.bindValue(":telephone", '8(8553) 314-110')
#         query.bindValue(":fax", ' 8(8553) 314-218')
#         query.bindValue(":inn_number", 1644011638)
#         query.bindValue(":kpp_number", 164401001)
#         query.bindValue(":ogrn_number", 1021601625561)
#         query.bindValue(":license_opo", test_BLOB)
#         query.bindValue(":reg_opo", test_BLOB)
#         query.bindValue(":position_pk", test_BLOB)
#         query.bindValue(":position_crash", test_BLOB)
#         query.exec_()
#
#         #                             vvv
#         q.exec_("DROP TABLE IF EXISTS opo;")
#         q.exec_("CREATE TABLE opo ("
#                 "id INT PRIMARY KEY, "
#                 "id_company INT NOT NULL, "
#                 "name_opo TEXT NOT NULL, "
#                 "address_opo TEXT NOT NULL, "
#                 "reg_number_opo TEXT NOT NULL, "
#                 "class_opo TEXT NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO opo (id, id_company, name_opo, "
#                       "address_opo, reg_number_opo, class_opo)"
#                       "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_company", 1)
#         query.bindValue(":name_opo", 'Фонд скважин Муслюмовского месторождения нефти и газа')
#         query.bindValue(":address_opo", 'РФ, РТ, Муслюмовский, Азнакаевский и Сармановский районы')
#         query.bindValue(":reg_number_opo", 'А43-01341-0005')
#         query.bindValue(":class_opo", '3')
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO opo (id, id_company, name_opo, "
#                       "address_opo, reg_number_opo, class_opo)"
#                       "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_company", 2)
#         query.bindValue(":name_opo", 'Фонд скважин Урмышлинского месторождения нефти')
#         query.bindValue(":address_opo", 'РФ, РТ, Черемшанский район, Лениногорский районы')
#         query.bindValue(":reg_number_opo", 'А43-01109-0001')
#         query.bindValue(":class_opo", '3')
#         query.exec_()
#
#         #                             vvvvvvvvvvvvv
#         q.exec_("DROP TABLE IF EXISTS documentation;")
#         q.exec_("CREATE TABLE documentation ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "type_doc TEXT NOT NULL, "
#                 "reg_doc TEXT NOT NULL, "
#                 "date_doc TEXT NOT NULL, "
#                 "doc BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO documentation (id, id_opo, type_doc, reg_doc, date_doc, doc)"
#                       "VALUES (:id, :id_opo, :type_doc, :reg_doc,:date_doc, :doc)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":type_doc", 'Декларция промышленной безопасности')
#         query.bindValue(":reg_doc", '43-ДПБ-00001-01')
#         query.bindValue(":date_doc", '14-12-2018')
#         query.bindValue(":doc", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO documentation (id, id_opo, type_doc, reg_doc, date_doc, doc)"
#                       "VALUES (:id, :id_opo, :type_doc, :reg_doc,:date_doc, :doc)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":type_doc", 'Консервация насоса Н-1')
#         query.bindValue(":reg_doc", '43-ЭПБ-00003-05')
#         query.bindValue(":date_doc", '25-07-2021')
#         query.bindValue(":doc", test_BLOB)
#         query.exec_()
#
#         #                             vvvvvvvv
#         q.exec_("DROP TABLE IF EXISTS line_obj;")
#         q.exec_("CREATE TABLE line_obj ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "reg_number INT NOT NULL, "
#                 "name_obj TEXT NOT NULL, "
#                 "substance TEXT NOT NULL, "
#                 "lenght DECIMAL NOT NULL, "
#                 "diameter DECIMAL NOT NULL, "
#                 "pressure DECIMAL NOT NULL, "
#                 "status TEXT NOT NULL, "
#                 "date_manufacture TEXT NOT NULL, "
#                 "date_entry TEXT NOT NULL, "
#                 "date_upto TEXT NOT NULL, "
#                 "passport BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO line_obj (id, id_opo, reg_number, name_obj, substance, lenght,"
#                       "diameter, pressure, status, date_manufacture, date_entry, date_upto, passport)"
#                       "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :lenght,"
#                       ":diameter, :pressure, :status, :date_manufacture, :date_entry, :date_upto, :passport)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":reg_number", '1258')
#         query.bindValue(":name_obj", 'Трубопровод')
#         query.bindValue(":substance", 'нефть')
#         query.bindValue(":lenght", 1.225)
#         query.bindValue(":diameter", 229)
#         query.bindValue(":pressure", 0.23)
#         query.bindValue(":status", 'Действующий')
#         query.bindValue(":date_manufacture", '01-01-1988')
#         query.bindValue(":date_entry", '01-05-1988')
#         query.bindValue(":date_upto", '01-01-2020')
#         query.bindValue(":passport", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO line_obj (id, id_opo, reg_number, name_obj, substance, lenght,"
#                       "diameter, pressure, status, date_manufacture, date_entry, date_upto, passport)"
#                       "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :lenght,"
#                       ":diameter, :pressure, :status, :date_manufacture, :date_entry, :date_upto, :passport)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":reg_number", '1347')
#         query.bindValue(":name_obj", 'Трубопровод')
#         query.bindValue(":substance", 'нефтяная эмульсия')
#         query.bindValue(":lenght", 5.03)
#         query.bindValue(":diameter", 114)
#         query.bindValue(":pressure", 0.56)
#         query.bindValue(":status", 'Законсервирован')
#         query.bindValue(":date_manufacture", '01-01-1995')
#         query.bindValue(":date_entry", '01-05-1996')
#         query.bindValue(":date_upto", '01-01-2025')
#         query.bindValue(":passport", test_BLOB)
#         query.exec_()
#
#         #                             vvvvvvvvv
#         q.exec_("DROP TABLE IF EXISTS state_obj;")
#         q.exec_("CREATE TABLE state_obj ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "reg_number INT NOT NULL, "
#                 "name_obj TEXT NOT NULL, "
#                 "substance TEXT NOT NULL, "
#                 "volume DECIMAL NOT NULL, "
#                 "temperature DECIMAL NOT NULL, "
#                 "pressure DECIMAL NOT NULL, "
#                 "alpha DECIMAL NOT NULL, "
#                 "status TEXT NOT NULL, "
#                 "date_manufacture TEXT NOT NULL, "
#                 "date_entry TEXT NOT NULL, "
#                 "date_upto TEXT NOT NULL, "
#                 "passport BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO state_obj (id, id_opo, reg_number, name_obj, substance, volume,"
#                       "temperature, pressure, alpha, status, date_manufacture, date_entry, date_upto, passport)"
#                       "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :volume,"
#                       ":temperature, :pressure, :alpha, :status, :date_manufacture, :date_entry, :date_upto, :passport)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":reg_number", '12589')
#         query.bindValue(":name_obj", 'Емкость Е-1')
#         query.bindValue(":substance", 'нефть')
#         query.bindValue(":volume", 200)
#         query.bindValue(":temperature", 55)
#         query.bindValue(":pressure", 0.23)
#         query.bindValue(":alpha", 0.25)
#         query.bindValue(":status", 'Действующий')
#         query.bindValue(":date_manufacture", '01-01-1988')
#         query.bindValue(":date_entry", '01-05-1988')
#         query.bindValue(":date_upto", '01-01-2020')
#         query.bindValue(":passport", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO state_obj (id, id_opo, reg_number, name_obj, substance, volume,"
#                       "temperature, pressure, alpha, status, date_manufacture, date_entry, date_upto, passport)"
#                       "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :volume,"
#                       ":temperature, :pressure, :alpha, :status, :date_manufacture, :date_entry, :date_upto, :passport)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":reg_number", '2589')
#         query.bindValue(":name_obj", 'Нефтесепаратор НГС-2')
#         query.bindValue(":substance", 'нефть')
#         query.bindValue(":volume", 100)
#         query.bindValue(":temperature", 55)
#         query.bindValue(":pressure", 0.23)
#         query.bindValue(":alpha", 0.25)
#         query.bindValue(":status", 'Действующий')
#         query.bindValue(":date_manufacture", '01-01-2005')
#         query.bindValue(":date_entry", '01-05-2006')
#         query.bindValue(":date_upto", '01-01-2027')
#         query.bindValue(":passport", test_BLOB)
#         query.exec_()
#
#         #                             vvvvvvvvvv
#         q.exec_("DROP TABLE IF EXISTS build_obj;")
#         q.exec_("CREATE TABLE build_obj ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "name_obj TEXT NOT NULL, "
#                 "status TEXT NOT NULL, "
#                 "date_manufacture TEXT NOT NULL, "
#                 "date_entry TEXT NOT NULL, "
#                 "date_upto TEXT NOT NULL, "
#                 "doc BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO build_obj (id, id_opo, name_obj, status, "
#                       "date_manufacture, date_entry, date_upto, doc)"
#                       "VALUES (:id, :id_opo, :name_obj, :status, :date_manufacture, :date_entry, "
#                       ":date_upto, :doc)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":name_obj", 'Операторная')
#         query.bindValue(":status", 'Консервация')
#         query.bindValue(":date_manufacture", '14-12-2018')
#         query.bindValue(":date_entry", '14-12-2018')
#         query.bindValue(":date_upto", '14-12-2028')
#         query.bindValue(":doc", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO build_obj (id, id_opo, name_obj, status, "
#                       "date_manufacture, date_entry, date_upto, doc)"
#                       "VALUES (:id, :id_opo, :name_obj, :status, :date_manufacture, :date_entry, "
#                       ":date_upto, :doc)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":name_obj", 'Лаборатория')
#         query.bindValue(":status", 'Дествующая')
#         query.bindValue(":date_manufacture", '14-12-2010')
#         query.bindValue(":date_entry", '14-12-2013')
#         query.bindValue(":date_upto", '14-12-2038')
#         query.bindValue(":doc", test_BLOB)
#         query.exec_()
#
#         #                             vvvvvvv
#         q.exec_("DROP TABLE IF EXISTS project;")
#         q.exec_("CREATE TABLE project ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "name_project TEXT NOT NULL, "
#                 "date_project TEXT NOT NULL, "
#                 "pz_project BLOB NOT NULL, "
#                 "pzu_project BLOB NOT NULL, "
#                 "kr_project BLOB NOT NULL, "
#                 "ios_project BLOB NOT NULL, "
#                 "pos_project BLOB NOT NULL, "
#                 "another_project BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO project (id, id_opo, name_project, date_project, "
#                       "pz_project, pzu_project, kr_project, ios_project,"
#                       "pos_project, another_project)"
#                       "VALUES (:id, :id_opo, :name_project, :date_project, :pz_project, :pzu_project, "
#                       ":kr_project, :ios_project, :pos_project, :another_project)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":name_project", 'Обустройство кустов скважин')
#         query.bindValue(":date_project", '14-12-2018')
#         query.bindValue(":pz_project", test_BLOB)
#         query.bindValue(":pzu_project", test_BLOB)
#         query.bindValue(":kr_project", test_BLOB)
#         query.bindValue(":ios_project", test_BLOB)
#         query.bindValue(":pos_project", test_BLOB)
#         query.bindValue(":another_project", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO project (id, id_opo, name_project, date_project, "
#                       "pz_project, pzu_project, kr_project, ios_project,"
#                       "pos_project, another_project)"
#                       "VALUES (:id, :id_opo, :name_project, :date_project, :pz_project, :pzu_project, "
#                       ":kr_project, :ios_project, :pos_project, :another_project)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":name_project", 'Обустройство куста скважин')
#         query.bindValue(":date_project", '14-12-2015')
#         query.bindValue(":pz_project", test_BLOB)
#         query.bindValue(":pzu_project", test_BLOB)
#         query.bindValue(":kr_project", test_BLOB)
#         query.bindValue(":ios_project", test_BLOB)
#         query.bindValue(":pos_project", test_BLOB)
#         query.bindValue(":another_project", test_BLOB)
#         query.exec_()
#
#         #                             vvv
#         q.exec_("DROP TABLE IF EXISTS epb;")
#         q.exec_("CREATE TABLE epb ("
#                 "id INT PRIMARY KEY, "
#                 "id_opo INT NOT NULL, "
#                 "name_doc TEXT NOT NULL, "
#                 "date_doc TEXT NOT NULL, "
#                 "epb_doc BLOB NOT NULL );")
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO epb (id, id_opo, name_doc, date_doc, epb_doc)"
#                       "VALUES (:id, :id_opo, :name_doc, :date_doc, :epb_doc)")
#
#         query.bindValue(":id", 1)
#         query.bindValue(":id_opo", 1)
#         query.bindValue(":name_doc", 'ЭПБ на задвижку')
#         query.bindValue(":date_doc", '14-12-2018')
#         query.bindValue(":epb_doc", test_BLOB)
#         query.exec_()
#
#         query = QtSql.QSqlQuery()
#         query.prepare("INSERT INTO epb (id, id_opo, name_doc, date_doc, epb_doc)"
#                       "VALUES (:id, :id_opo, :name_doc, :date_doc, :epb_doc)")
#
#         query.bindValue(":id", 2)
#         query.bindValue(":id_opo", 2)
#         query.bindValue(":name_doc", 'ЭПБ на трубу')
#         query.bindValue(":date_doc", '14-12-2018')
#         query.bindValue(":epb_doc", test_BLOB)
#         query.exec_()
#
#         self.db.commit()
#
#     def createModel(self, table_state):
#         """
#         Создание модели для отображения
#         """
#         self.model = SQL_table_whith_ico(db=self.db, select=table_state)
#         # self.model.setTable("company")
#         # # self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
#         # # self.model.setHeaderData(1, QtCore.Qt.Horizontal, "НаименованиеОПО")
#         # # self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Наименование ЭПБ")
#         # # self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Дата")
#         # # self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Док-ты")
#         # # self.set_relation()
#         self.model.select()
#
#
#     def table_select(self, text):
#         if text == "Компании":
#             self.model = SQL_table_whith_ico(db=self.db, select=self.table_box.currentText())
#             self.model.setTable("company")
#             self.model.select()
#         elif text == "ОПО":
#             pass
#         elif text == "Документация ОПО":
#             pass
#         elif text == "Линейные объекты":
#             pass
#         elif text == "Стационарные объекты":
#             pass
#         elif text == "Здания и сооружения":
#             pass
#         elif text == "Проекты":
#             pass
#         elif text == "Экспертизы пром.безопасности":
#             self.model.setTable("epb")
#             self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование ОПО")
#             self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Наименование экспертизы")
#             self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Дата утверждения")
#             self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Экспертиза")
#             self.set_relation()
#             self.model.select()
#
#     def any_table(self):
#         print('1')
#         self.model.setTable("company")
#         # self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
#         # self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование организации")
#         # self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Наименование ОПО")
#         # self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Адрес ОПО")
#         # self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Рег.номер ОПО")
#         # self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Класс ОПО")
#         # self.model.setHeaderData(6, QtCore.Qt.Horizontal, "Свидетельство о регистрации")
#         # self.set_relation()
#         self.model.select()
#         print("2")
#
#     def closeEvent(self, event):
#         if (self.db.open()):
#             self.db.close()
#
#     def set_relation(self):
#         self.model.setRelation(1, QtSql.QSqlRelation(
#             "opo",
#             "id",
#             "name_opo"
#         ))
#
#     def addRecord(self):
#         inputDialog = Dialog()
#         rez = inputDialog.exec()
#         if not rez:
#             msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
#             return
#
#         name = inputDialog.line_edit_name.text()
#         quantity = inputDialog.line_edit_quantity.text()
#         category = inputDialog.line_edit_category.text()
#         if (not name) or (not quantity) or (not category):
#             msg = QtWidgets.QMessageBox.information(self,
#                                                     'Внимание', 'Заполните пожалуйста все поля.')
#             return
#
#         r = self.model.record()
#         r.setValue(0, name)
#         r.setValue(1, int(quantity))
#         r.setValue(2, int(category))
#
#         self.model.insertRecord(-1, r)
#         self.model.select()
#
#     def delRecord(self):
#         row = self.view.currentIndex().row()
#         if row == -1:
#             msg = QtWidgets.QMessageBox.information(self,
#                                                     'Внимание', 'Выберите запись для удаления.')
#             return
#
#         name = self.model.record(row).value(0)
#         quantity = self.model.record(row).value(1)
#         category = self.model.record(row).value(2)
#
#         inputDialog = Dialog()
#         inputDialog.setWindowTitle('Удалить запись ???')
#         inputDialog.line_edit_name.setText(name)
#         inputDialog.line_edit_quantity.setText(str(quantity))
#         inputDialog.line_edit_category.setText(str(category))
#         rez = inputDialog.exec()
#         if not rez:
#             msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
#             return
#
#         self.model.setRelation(2, QtSql.QSqlRelation())
#         self.model.select()
#         self.model.removeRow(row)
#         self.set_relation()
#         self.model.select()
#
#         msg = QtWidgets.QMessageBox.information(self, 'Успех', 'Запись удалена.')
#
#     def convertToBinaryData(self, file_path):
#         # Конвертирование в BLOB
#         with open(file_path, 'rb') as file:
#             blobData = file.read()
#             print()
#         return blobData
#
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     app.setStyle('Fusion')
#     w = Storage_app()
#     app.exec_()

