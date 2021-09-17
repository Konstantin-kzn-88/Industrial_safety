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
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlRelationalTableModel


class Add_Dialog(QtWidgets.QDialog):
    def __init__(self, state="company", id=100, list_for_combo=[]):
        super().__init__()
        main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        folder_file = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/folder_file.png')
        onlyInt = QtGui.QIntValidator()
        self.setWindowIcon(main_ico)

        if state == "company":
            self.setWindowTitle('Добавление организации')
            self.id_company = QtWidgets.QLineEdit()
            self.id_company.setText(str(id))
            self.id_company.setReadOnly(True)
            self.name_company = QtWidgets.QLineEdit()
            self.full_name_manager = QtWidgets.QLineEdit()
            self.ur_address = QtWidgets.QLineEdit()
            self.post_address = QtWidgets.QLineEdit()
            self.email = QtWidgets.QLineEdit()
            self.telephone = QtWidgets.QLineEdit()
            self.fax = QtWidgets.QLineEdit()
            self.inn_number = QtWidgets.QLineEdit()
            self.inn_number.setValidator(onlyInt)
            self.kpp_number = QtWidgets.QLineEdit()
            self.kpp_number.setValidator(onlyInt)
            self.ogrn_number = QtWidgets.QLineEdit()
            self.ogrn_number.setValidator(onlyInt)
            # лицензия
            self.license_opo = QtWidgets.QLineEdit()
            self.license_opo.setReadOnly(True)
            self.license_opo_btn = QtWidgets.QPushButton("", objectName="license_opo_btn")
            self.license_opo_btn.setIcon(folder_file)
            self.license_opo_btn.clicked.connect(self.file_path)
            license_hbox = QtWidgets.QHBoxLayout()
            license_hbox.addWidget(self.license_opo)
            license_hbox.addWidget(self.license_opo_btn)
            # регистрация ОПО
            self.reg_opo = QtWidgets.QLineEdit()
            self.reg_opo.setReadOnly(True)
            self.reg_opo_btn = QtWidgets.QPushButton("", objectName="reg_opo_btn")
            self.reg_opo_btn.setIcon(folder_file)
            self.reg_opo_btn.clicked.connect(self.file_path)
            reg_hbox = QtWidgets.QHBoxLayout()
            reg_hbox.addWidget(self.reg_opo)
            reg_hbox.addWidget(self.reg_opo_btn)
            # Положение о ПК
            self.position_pk = QtWidgets.QLineEdit()
            self.position_pk.setReadOnly(True)
            self.position_pk_btn = QtWidgets.QPushButton("", objectName="position_pk_btn")
            self.position_pk_btn.setIcon(folder_file)
            self.position_pk_btn.clicked.connect(self.file_path)
            pk_hbox = QtWidgets.QHBoxLayout()
            pk_hbox.addWidget(self.position_pk)
            pk_hbox.addWidget(self.position_pk_btn)
            # Положение об авариях
            self.position_crash = QtWidgets.QLineEdit()
            self.position_crash.setReadOnly(True)
            self.position_crash_btn = QtWidgets.QPushButton("", objectName="position_crash_btn")
            self.position_crash_btn.setIcon(folder_file)
            self.position_crash_btn.clicked.connect(self.file_path)
            crash_hbox = QtWidgets.QHBoxLayout()
            crash_hbox.addWidget(self.position_crash)
            crash_hbox.addWidget(self.position_crash_btn)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_company)
            form_layout.addRow('Наименование организации: ', self.name_company)
            form_layout.addRow('Ф.И.О. руководителя: ', self.full_name_manager)
            form_layout.addRow('Юр.адрес ', self.ur_address)
            form_layout.addRow('Почтовый адрес: ', self.post_address)
            form_layout.addRow('Email :', self.email)
            form_layout.addRow('Телефон: ', self.telephone)
            form_layout.addRow('Факс :', self.fax)
            form_layout.addRow('ИНН :', self.inn_number)
            form_layout.addRow('КПП: ', self.kpp_number)
            form_layout.addRow('ОГРН :', self.ogrn_number)
            form_layout.addRow('Лицензия :', license_hbox)
            form_layout.addRow('Регистрация ОПО: ', reg_hbox)
            form_layout.addRow('Производственный контроль :', pk_hbox)
            form_layout.addRow('Положение (аварии) :', crash_hbox)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

        elif state == "opo":
            self.setWindowTitle('Добавление опасного объекта')
            self.id_opo = QtWidgets.QLineEdit()
            self.id_opo.setText(str(id))
            self.id_opo.setReadOnly(True)
            self.id_company = QtWidgets.QComboBox()
            self.id_company.addItems(list_for_combo)
            self.name_opo = QtWidgets.QLineEdit()
            self.address_opo = QtWidgets.QLineEdit()
            self.reg_number_opo = QtWidgets.QLineEdit()
            self.class_opo = QtWidgets.QLineEdit()
            self.class_opo.setValidator(onlyInt)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_opo)
            form_layout.addRow('Наименование организации: ', self.id_company)
            form_layout.addRow('Наименование ОПО: ', self.name_opo)
            form_layout.addRow('Адрес ОПО: ', self.address_opo)
            form_layout.addRow('Рег № ОПО: ', self.reg_number_opo)
            form_layout.addRow('Класс опасности: ', self.class_opo)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

        elif state == 'documentation':
            self.setWindowTitle('Добавление документации ОПО')
            self.id_doc = QtWidgets.QLineEdit()
            self.id_doc.setText(str(id))
            self.id_doc.setReadOnly(True)
            self.id_opo = QtWidgets.QComboBox()
            self.id_opo.addItems(list_for_combo)
            self.type_doc = QtWidgets.QLineEdit()
            self.reg_doc = QtWidgets.QLineEdit()
            self.date_doc = QtWidgets.QLineEdit()
            # Документация ОПО
            self.doc_opo = QtWidgets.QLineEdit()
            self.doc_opo.setReadOnly(True)
            self.doc_opo_btn = QtWidgets.QPushButton("", objectName="doc_opo_btn")
            self.doc_opo_btn.setIcon(folder_file)
            self.doc_opo_btn.clicked.connect(self.file_path)
            doc_hbox = QtWidgets.QHBoxLayout()
            doc_hbox.addWidget(self.doc_opo)
            doc_hbox.addWidget(self.doc_opo_btn)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_doc)
            form_layout.addRow('Наименование ОПО: ', self.id_opo)
            form_layout.addRow('Наименование документации: ', self.type_doc)
            form_layout.addRow('Рег. № документации: ', self.reg_doc)
            form_layout.addRow('Дата: ', self.date_doc)
            form_layout.addRow('Документация: ', doc_hbox)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

        elif state == 'line_obj':
            self.setWindowTitle('Добавление линейного объекта')
            self.id_line = QtWidgets.QLineEdit()
            self.id_line.setText(str(id))
            self.id_line.setReadOnly(True)
            self.id_opo = QtWidgets.QComboBox()
            self.id_opo.addItems(list_for_combo)
            self.reg_number = QtWidgets.QLineEdit()
            self.reg_number.setValidator(onlyInt)
            self.name_obj = QtWidgets.QLineEdit()
            self.substance = QtWidgets.QLineEdit()
            self.lenght = QtWidgets.QLineEdit()
            self.lenght.setValidator(onlyInt)
            self.diameter = QtWidgets.QLineEdit()
            self.diameter.setValidator(onlyInt)
            self.pressure = QtWidgets.QLineEdit()
            self.pressure.setValidator(onlyInt)
            self.status = QtWidgets.QLineEdit()
            self.date_manufacture = QtWidgets.QLineEdit()
            self.date_entry = QtWidgets.QLineEdit()
            self.date_upto = QtWidgets.QLineEdit()
            # Паспорт
            self.passport = QtWidgets.QLineEdit()
            self.passport.setReadOnly(True)
            self.passport_btn = QtWidgets.QPushButton("", objectName="passport_btn")
            self.passport_btn.setIcon(folder_file)
            self.passport_btn.clicked.connect(self.file_path)
            passport_hbox = QtWidgets.QHBoxLayout()
            passport_hbox.addWidget(self.passport)
            passport_hbox.addWidget(self.passport_btn)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_line)
            form_layout.addRow('Наименование ОПО: ', self.id_opo)
            form_layout.addRow('Рег. №: ', self.reg_number)
            form_layout.addRow('Наименование оборудования: ', self.name_obj)
            form_layout.addRow('Вещество: ', self.substance)
            form_layout.addRow('Длина, м: ', self.lenght)
            form_layout.addRow('Диаметр, мм: ', self.diameter)
            form_layout.addRow('Давление, МПа: ', self.pressure)
            form_layout.addRow('Статус: ', self.status)
            form_layout.addRow('Дата изготовления: ', self.date_manufacture)
            form_layout.addRow('Дата ввода: ', self.date_entry)
            form_layout.addRow('Эксплуатировать до: ', self.date_upto)
            form_layout.addRow('Паспорт: ', passport_hbox)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

        elif state == 'state_obj':
            self.setWindowTitle('Добавление стационарного объекта')
            self.id_state = QtWidgets.QLineEdit()
            self.id_state.setText(str(id))
            self.id_state.setReadOnly(True)
            self.id_opo = QtWidgets.QComboBox()
            self.id_opo.addItems(list_for_combo)
            self.reg_number = QtWidgets.QLineEdit()
            self.reg_number.setValidator(onlyInt)
            self.name_obj = QtWidgets.QLineEdit()
            self.substance = QtWidgets.QLineEdit()
            self.volume = QtWidgets.QLineEdit()
            self.volume.setValidator(onlyInt)
            self.temperature = QtWidgets.QLineEdit()
            self.temperature.setValidator(onlyInt)
            self.pressure = QtWidgets.QLineEdit()
            self.pressure.setValidator(onlyInt)
            self.alpha = QtWidgets.QLineEdit()
            self.alpha.setValidator(onlyInt)
            self.status = QtWidgets.QLineEdit()
            self.date_manufacture = QtWidgets.QLineEdit()
            self.date_entry = QtWidgets.QLineEdit()
            self.date_upto = QtWidgets.QLineEdit()
            # Паспорт
            self.passport_st = QtWidgets.QLineEdit()
            self.passport_st.setReadOnly(True)
            self.passport_st_btn = QtWidgets.QPushButton("", objectName="passport_st_btn")
            self.passport_st_btn.setIcon(folder_file)
            self.passport_st_btn.clicked.connect(self.file_path)
            passport_hbox = QtWidgets.QHBoxLayout()
            passport_hbox.addWidget(self.passport_st)
            passport_hbox.addWidget(self.passport_st_btn)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_state)
            form_layout.addRow('Наименование ОПО: ', self.id_opo)
            form_layout.addRow('Рег. №: ', self.reg_number)
            form_layout.addRow('Наименование оборудования: ', self.name_obj)
            form_layout.addRow('Вещество: ', self.substance)
            form_layout.addRow('Объем, м3: ', self.volume)
            form_layout.addRow('Температура, С: ', self.temperature)
            form_layout.addRow('Давление, МПа: ', self.pressure)
            form_layout.addRow('Ст.заполнения, -: ', self.alpha)
            form_layout.addRow('Статус: ', self.status)
            form_layout.addRow('Дата изготовления: ', self.date_manufacture)
            form_layout.addRow('Дата ввода: ', self.date_entry)
            form_layout.addRow('Эксплуатировать до: ', self.date_upto)
            form_layout.addRow('Паспорт: ', passport_hbox)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

        elif state == 'build_obj':
            self.setWindowTitle('Добавление здания/сооружения')
            self.id_build = QtWidgets.QLineEdit()
            self.id_build.setText(str(id))
            self.id_build.setReadOnly(True)
            self.id_opo = QtWidgets.QComboBox()
            self.id_opo.addItems(list_for_combo)
            self.name_obj = QtWidgets.QLineEdit()
            self.status = QtWidgets.QLineEdit()
            self.date_manufacture = QtWidgets.QLineEdit()
            self.date_entry = QtWidgets.QLineEdit()
            self.date_upto = QtWidgets.QLineEdit()
            # Паспорт
            self.passport_build = QtWidgets.QLineEdit()
            self.passport_build.setReadOnly(True)
            self.passport_build_btn = QtWidgets.QPushButton("", objectName="passport_build_btn")
            self.passport_build_btn.setIcon(folder_file)
            self.passport_build_btn.clicked.connect(self.file_path)
            passport_hbox = QtWidgets.QHBoxLayout()
            passport_hbox.addWidget(self.passport_build)
            passport_hbox.addWidget(self.passport_build_btn)

            form_layout = QtWidgets.QFormLayout()
            form_layout.addRow('id: ', self.id_build)
            form_layout.addRow('Наименование ОПО: ', self.id_opo)
            form_layout.addRow('Наименование здания/сооружения: ', self.name_obj)
            form_layout.addRow('Статус: ', self.status)
            form_layout.addRow('Дата изготовления: ', self.date_manufacture)
            form_layout.addRow('Дата ввода: ', self.date_entry)
            form_layout.addRow('Эксплуатировать до: ', self.date_upto)
            form_layout.addRow('Паспорт: ', passport_hbox)

            button_box = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.addLayout(form_layout)
            main_layout.addWidget(button_box)

    def file_path(self):
        sender = self.sender()
        path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     'Документ для внесения в базу данных',
                                                     ".", ("PDF (*.pdf)"))[0]
        if path == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Файл не выбран")
            msg.exec()
            return

        if sender.objectName() == "license_opo_btn":
            self.license_opo.setText(path)
        elif sender.objectName() == "reg_opo_btn":
            self.reg_opo.setText(path)
        elif sender.objectName() == "position_pk_btn":
            self.position_pk.setText(path)
        elif sender.objectName() == "position_crash_btn":
            self.position_crash.setText(path)
        elif sender.objectName() == "doc_opo_btn":
            self.doc_opo.setText(path)
        elif sender.objectName() == "passport_btn":
            self.passport.setText(path)
        elif sender.objectName() == "passport_st_btn":
            self.passport_st.setText(path)
        elif sender.objectName() == "passport_build_btn":
            self.passport_build.setText(path)

        return


class Relational_table_model_with_icon(QSqlRelationalTableModel):
    def __init__(self, state="company", **kwargs):
        self.state = state
        QSqlRelationalTableModel.__init__(self, **kwargs)

    def setState(self, state):
        # Обновление данных
        self.state = state
        i_start = self.index(0, 0)
        i_end = self.index(self.rowCount() - 1, 20)
        # print(self.state)
        if self.state == "company":
            i_start = self.index(0, 11)
            i_end = self.index(self.rowCount() - 1, 14)
        elif self.state == "opo":
            i_start = self.index(0, 5)
            i_end = self.index(self.rowCount() - 1, 5)
        elif self.state == "documentation":
            i_start = self.index(0, 5)
            i_end = self.index(self.rowCount() - 1, 5)
        elif self.state == "line_obj":
            i_start = self.index(0, 12)
            i_end = self.index(self.rowCount() - 1, 13)
        elif self.state == "state_obj":
            i_start = self.index(0, 13)
            i_end = self.index(self.rowCount() - 1, 13)
        elif self.state == "build_obj":
            i_start = self.index(0, 7)
            i_end = self.index(self.rowCount() - 1, 7)
        elif self.state == "project":
            i_start = self.index(0, 4)
            i_end = self.index(self.rowCount() - 1, 9)
        elif self.state == "epb":
            i_start = self.index(0, 4)
            i_end = self.index(self.rowCount() - 1, 4)
        self.dataChanged.emit(i_start, i_end)

    def data(self, index, role=Qt.DisplayRole):
        icon = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
        if self.state == "company":
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
        elif self.state == "opo":
            pass
        elif self.state == "documentation":
            if index.column() == 5 and role == Qt.DisplayRole:
                return ""
            if index.column() == 5 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 4 and role == Qt.BackgroundRole:
                color = QtGui.QColor(200, 200, 200, 200)
                print(type(index.data()))
                return color
        elif self.state == "line_obj":
            if index.column() == 12 and role == Qt.DisplayRole:
                return ""
            if index.column() == 12 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
        elif self.state == "state_obj":
            if index.column() == 13 and role == Qt.DisplayRole:
                return ""
            if index.column() == 13 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
        elif self.state == "build_obj":
            if index.column() == 7 and role == Qt.DisplayRole:
                return ""
            if index.column() == 7 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
        elif self.state == "project":
            if index.column() == 4 and role == Qt.DisplayRole:
                return ""
            if index.column() == 4 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 5 and role == Qt.DisplayRole:
                return ""
            if index.column() == 5 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 6 and role == Qt.DisplayRole:
                return ""
            if index.column() == 6 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 7 and role == Qt.DisplayRole:
                return ""
            if index.column() == 7 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 8 and role == Qt.DisplayRole:
                return ""
            if index.column() == 8 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
            if index.column() == 9 and role == Qt.DisplayRole:
                return ""
            if index.column() == 9 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)
        elif self.state == "epb":
            if index.column() == 4 and role == Qt.DisplayRole:
                return ""
            if index.column() == 4 and role == Qt.DecorationRole:
                return QtGui.QIcon(icon)

        return QSqlRelationalTableModel.data(self, index,
                                             role)  # все остальное должно штатно обработаться qsqltablemodel


class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.table_box_state = "company"
        self.createConnection()
        # self.fillTable()

        self.createModel()
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.initUI()
        #     Структура данных (словари для корректности работы БД)
        self.list_id_company = []

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
        self.model = Relational_table_model_with_icon(db=self.db, state=self.table_box_state)
        self.model.setTable("company")
        self.model.select()

    def initUI(self):
        # Иконки
        self.table_state = "company"
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/data_base.png')
        company_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/company.png')
        state_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/state.png')
        plus_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/plus.png')
        minus_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/minus.png')
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
        grid.setColumnStretch(0, 9)
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
        self.table_box.activated[str].connect(self.table_select)

        self.add_in_db = QtWidgets.QPushButton("Добавить строку")
        self.add_in_db.setIcon(plus_ico)
        self.add_in_db.setToolTip("Добавить строку в таблицу")
        self.add_in_db.clicked.connect(self.add_in_data_base)
        self.del_from_db = QtWidgets.QPushButton("Удалить строку")
        self.del_from_db.setIcon(minus_ico)
        self.del_from_db.setToolTip("Удалить строку из таблицу")
        self.del_from_db.clicked.connect(self.delete_from_data_base)
        self.edit_from_db = QtWidgets.QPushButton("Редактировать")
        self.edit_from_db.setIcon(minus_ico)
        self.edit_from_db.setToolTip("Редактировать выделенный элемент")
        self.edit_from_db.clicked.connect(self.edit_from_data_base)

        # Упаковываем все на вкладку таба "0" (делаем все в QGroupBox
        # т.к. элементы будут добавляться и их
        # потом нужно будет объединять в группы

        # Рамка №0
        layout_table_select = QtWidgets.QFormLayout(self)
        GB_table_select = QtWidgets.QGroupBox('Таблица базы данных')
        GB_table_select.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_table_select.addRow("", self.table_box)
        GB_table_select.setLayout(layout_table_select)
        # Рамка №1
        layout_table_edit = QtWidgets.QFormLayout(self)
        GB_table_edit = QtWidgets.QGroupBox('Добавить/удалить/редактировать позицию')
        GB_table_edit.setStyleSheet("QGroupBox { font-weight : bold; }")
        hbox_1 = QtWidgets.QHBoxLayout()
        hbox_1.addWidget(self.add_in_db)
        hbox_1.addWidget(self.del_from_db)
        hbox_1.addWidget(self.edit_from_db)
        layout_table_edit.addRow("", hbox_1)
        GB_table_edit.setLayout(layout_table_edit)
        # Собираем рамки
        self.tab_main.layout.addWidget(GB_table_select)
        self.tab_main.layout.addWidget(GB_table_edit)
        # Размещаем на табе
        self.tab_main.setLayout(self.tab_main.layout)
        # Размещаем на сетке
        grid.addWidget(self.view, 0, 0, 1, 1)
        grid.addWidget(self.tabs, 0, 1, 1, 1)
        self.centralWidget.setLayout(grid)
        self.setCentralWidget(self.centralWidget)

    def table_select(self, text):
        # self.model.data()
        if text == 'Компании':
            self.table_box_state = "company"
            self.model.setState(self.table_box_state)
            self.model.setTable("company")
            self.model.select()
        if text == 'ОПО':
            self.table_box_state = "opo"
            self.model.setState(self.table_box_state)
            self.model.setTable("opo")
            self.model.select()
        elif text == 'Документация ОПО':
            self.table_box_state = "documentation"
            self.model.setState(self.table_box_state)
            self.model.setTable("documentation")
            self.model.select()
        elif text == 'Линейные объекты':
            self.table_box_state = "line_obj"
            self.model.setState(self.table_box_state)
            self.model.setTable("line_obj")
            self.model.select()
        elif text == 'Стационарные объекты':
            self.table_box_state = "state_obj"
            self.model.setState(self.table_box_state)
            self.model.setTable("state_obj")
            self.model.select()
        elif text == 'Здания и сооружения':
            self.table_box_state = "build_obj"
            self.model.setState(self.table_box_state)
            self.model.setTable("build_obj")
            self.model.select()
        elif text == 'Проекты':
            self.table_box_state = "project"
            self.model.setState(self.table_box_state)
            self.model.setTable("project")
            self.model.select()
        elif text == 'Экспертизы пром.безопасности':
            self.table_box_state = "epb"
            self.model.setState(self.table_box_state)
            self.model.setTable("epb")
            self.model.select()

    def add_in_data_base(self):

        def fill_combobox(table_box_state):
            list_name = []
            if table_box_state == 'opo':
                query = QtSql.QSqlQuery('SELECT * FROM company')
                while query.next():
                    list_name.append(str(query.value(0)) + " " + query.value(1))
                query.exec_()
            else:
                query = QtSql.QSqlQuery('SELECT * FROM opo')
                while query.next():
                    list_name.append(str(query.value(0)) + " " + query.value(2))
                query.exec_()
            return list_name

        list_name = fill_combobox(self.table_box_state)

        # Определим максимальный id
        list_id = []
        max_id = 0
        if self.model.rowCount() == 0:
            max_id = max_id + 1
        else:
            for row in range(self.model.rowCount()):
                for column in range(self.model.columnCount()):
                    if column == 0:
                        index = self.model.index(row, column)
                        list_id.append(index.data())
            max_id = max(list_id) + 1

        inputDialog = Add_Dialog(state=self.table_box_state, id=max_id, list_for_combo=list_name)
        rez = inputDialog.exec()
        if not rez:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание!', 'Добавление в базу данных отменено')
            return

        if self.table_box_state == 'company':
            id_company = inputDialog.id_company.text()
            name_company = inputDialog.name_company.text()
            full_name_manager = inputDialog.full_name_manager.text()
            ur_address = inputDialog.ur_address.text()
            post_address = inputDialog.post_address.text()
            email = inputDialog.email.text()
            telephone = inputDialog.telephone.text()
            fax = inputDialog.fax.text()
            inn_number = inputDialog.inn_number.text()
            kpp_number = inputDialog.kpp_number.text()
            ogrn_number = inputDialog.ogrn_number.text()
            license_opo = inputDialog.license_opo.text()
            reg_opo = inputDialog.reg_opo.text()
            position_pk = inputDialog.position_pk.text()
            position_crash = inputDialog.position_crash.text()

            list_data = [id_company, name_company, full_name_manager, ur_address,
                         post_address, email, telephone, fax, inn_number, kpp_number,
                         ogrn_number, license_opo, reg_opo, position_pk, position_crash]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            print("READY TO WRITE DB FOR COMPANY")

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO company (id, name_company, full_name_manager, "
                          "ur_address, post_address, telephone, email, fax, inn_number, kpp_number, ogrn_number, "
                          "license_opo, reg_opo, position_pk, position_crash) "
                          "VALUES (:id, :name_company, :full_name_manager, :ur_address,:post_address, :telephone, :email, "
                          ":fax, :inn_number, :kpp_number, :ogrn_number, :license_opo, :reg_opo, :position_pk, :position_crash)")

            query.bindValue(":id", id_company)
            query.bindValue(":name_company", name_company)
            query.bindValue(":full_name_manager", full_name_manager)
            query.bindValue(":ur_address", ur_address)
            query.bindValue(":post_address", post_address)
            query.bindValue(":email", email)
            query.bindValue(":telephone", telephone)
            query.bindValue(":fax", fax)
            query.bindValue(":inn_number", inn_number)
            query.bindValue(":kpp_number", kpp_number)
            query.bindValue(":ogrn_number", ogrn_number)
            query.bindValue(":license_opo", QtCore.QByteArray(self.convertToBinaryData(license_opo)))
            query.bindValue(":reg_opo", QtCore.QByteArray(self.convertToBinaryData(reg_opo)))
            query.bindValue(":position_pk", QtCore.QByteArray(self.convertToBinaryData(position_pk)))
            query.bindValue(":position_crash", QtCore.QByteArray(self.convertToBinaryData(position_crash)))
            query.exec_()

        if self.table_box_state == 'opo':
            id_opo = inputDialog.id_opo.text()
            curr_text = inputDialog.id_company.currentText()
            id_company = curr_text.split()[0]
            name_opo = inputDialog.name_opo.text()
            address_opo = inputDialog.address_opo.text()
            reg_number_opo = inputDialog.reg_number_opo.text()
            class_opo = inputDialog.class_opo.text()

            list_data = [id_opo, id_company, name_opo, reg_number_opo, class_opo]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            print("READY TO WRITE DB FOR COMPANY")

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO opo (id, id_company, name_opo, "
                          "address_opo, reg_number_opo, class_opo)"
                          "VALUES (:id, :id_company, :name_opo, :address_opo,:reg_number_opo, :class_opo)")

            query.bindValue(":id", id_opo)
            query.bindValue(":id_company", id_company)
            query.bindValue(":name_opo", name_opo)
            query.bindValue(":address_opo", address_opo)
            query.bindValue(":reg_number_opo", reg_number_opo)
            query.bindValue(":class_opo", class_opo)
            query.exec_()

        if self.table_box_state == 'documentation':
            id_doc = inputDialog.id_doc.text()
            curr_text = inputDialog.id_opo.currentText()
            id_opo = curr_text.split()[0]
            reg_doc = inputDialog.reg_doc.text()
            type_doc = inputDialog.type_doc.text()
            date_doc = inputDialog.date_doc.text()
            doc_opo = inputDialog.doc_opo.text()

            list_data = [id_doc, id_opo, type_doc, date_doc, doc_opo]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            print("READY TO WRITE DB FOR DOC")

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO documentation (id, id_opo, type_doc, reg_doc, date_doc, doc)"
                          "VALUES (:id, :id_opo, :type_doc, :reg_doc,:date_doc, :doc)")

            query.bindValue(":id", id_doc)
            query.bindValue(":id_opo", id_opo)
            query.bindValue(":type_doc", type_doc)
            query.bindValue(":reg_doc", reg_doc)
            query.bindValue(":date_doc", date_doc)
            query.bindValue(":doc", QtCore.QByteArray(self.convertToBinaryData(doc_opo)))
            query.exec_()

        if self.table_box_state == 'line_obj':
            id_line = inputDialog.id_line.text()
            curr_text = inputDialog.id_opo.currentText()
            id_opo = curr_text.split()[0]
            reg_number = inputDialog.reg_number.text()
            name_obj = inputDialog.name_obj.text()
            substance = inputDialog.substance.text()
            lenght = inputDialog.lenght.text()
            diameter = inputDialog.diameter.text()
            pressure = inputDialog.pressure.text()
            status = inputDialog.status.text()
            date_manufacture = inputDialog.date_manufacture.text()
            date_entry = inputDialog.date_entry.text()
            date_upto = inputDialog.date_upto.text()
            passport = inputDialog.passport.text()

            list_data = [id_line, id_opo, reg_number, name_obj, substance, lenght, diameter,
                         pressure, status, date_manufacture, date_entry,
                         date_upto, passport]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            print("READY TO WRITE DB FOR LINE")

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO line_obj (id, id_opo, reg_number, name_obj, substance, lenght,"
                          "diameter, pressure, status, date_manufacture, date_entry, date_upto, passport)"
                          "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :lenght,"
                          ":diameter, :pressure, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

            query.bindValue(":id", id_line)
            query.bindValue(":id_opo", id_opo)
            query.bindValue(":reg_number", reg_number)
            query.bindValue(":name_obj", name_obj)
            query.bindValue(":substance", substance)
            query.bindValue(":lenght", lenght)
            query.bindValue(":diameter", diameter)
            query.bindValue(":pressure", pressure)
            query.bindValue(":status", status)
            query.bindValue(":date_manufacture", date_manufacture)
            query.bindValue(":date_entry", date_entry)
            query.bindValue(":date_upto", date_upto)
            query.bindValue(":passport", QtCore.QByteArray(self.convertToBinaryData(passport)))
            query.exec_()

        if self.table_box_state == 'state_obj':
            id_state = inputDialog.id_state.text()
            curr_text = inputDialog.id_opo.currentText()
            id_opo = curr_text.split()[0]
            reg_number = inputDialog.reg_number.text()
            name_obj = inputDialog.name_obj.text()
            substance = inputDialog.substance.text()
            volume = inputDialog.volume.text()
            temperature = inputDialog.temperature.text()
            pressure = inputDialog.pressure.text()
            alpha = inputDialog.alpha.text()
            status = inputDialog.status.text()
            date_manufacture = inputDialog.date_manufacture.text()
            date_entry = inputDialog.date_entry.text()
            date_upto = inputDialog.date_upto.text()
            passport = inputDialog.passport_st.text()

            list_data = [id_state, id_opo, reg_number, name_obj, substance, volume, temperature,
                         pressure, alpha, status, date_manufacture, date_entry,
                         date_upto, passport]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO state_obj (id, id_opo, reg_number, name_obj, substance, volume,"
                          "temperature, pressure, alpha, status, date_manufacture, date_entry, date_upto, passport)"
                          "VALUES (:id, :id_opo, :reg_number, :name_obj,:substance, :volume,"
                          ":temperature, :pressure, :alpha, :status, :date_manufacture, :date_entry, :date_upto, :passport)")

            query.bindValue(":id", id_state)
            query.bindValue(":id_opo", id_opo)
            query.bindValue(":reg_number", reg_number)
            query.bindValue(":name_obj", name_obj)
            query.bindValue(":substance", substance)
            query.bindValue(":volume", volume)
            query.bindValue(":temperature", temperature)
            query.bindValue(":pressure", pressure)
            query.bindValue(":alpha", alpha)
            query.bindValue(":status", status)
            query.bindValue(":date_manufacture", date_manufacture)
            query.bindValue(":date_entry", date_entry)
            query.bindValue(":date_upto", date_upto)
            query.bindValue(":passport", QtCore.QByteArray(self.convertToBinaryData(passport)))
            query.exec_()

        if self.table_box_state == 'build_obj':
            id_build = inputDialog.id_build.text()
            curr_text = inputDialog.id_opo.currentText()
            id_opo = curr_text.split()[0]
            name_obj = inputDialog.name_obj.text()
            status = inputDialog.status.text()
            date_manufacture = inputDialog.date_manufacture.text()
            date_entry = inputDialog.date_entry.text()
            date_upto = inputDialog.date_upto.text()
            passport = inputDialog.passport_build.text()

            list_data = [id_build, id_opo, name_obj, status, date_manufacture, date_entry,
                         date_upto, passport]

            for i in list_data:
                if i == '':
                    msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                    return

            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO build_obj (id, id_opo, name_obj, status, "
                          "date_manufacture, date_entry, date_upto, doc)"
                          "VALUES (:id, :id_opo, :name_obj, :status, :date_manufacture, :date_entry, "
                          ":date_upto, :doc)")

            query.bindValue(":id", id_build)
            query.bindValue(":id_opo", id_opo)
            query.bindValue(":name_obj", name_obj)
            query.bindValue(":status", status)
            query.bindValue(":date_manufacture", date_manufacture)
            query.bindValue(":date_entry", date_entry)
            query.bindValue(":date_upto", date_upto)
            query.bindValue(":doc", passport)
            query.exec_()



        self.model.select()

    def delete_from_data_base(self):
        pass

    def edit_from_data_base(self):
        pass

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
