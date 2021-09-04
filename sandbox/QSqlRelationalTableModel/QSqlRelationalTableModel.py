import sys
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


class Example(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.createConnection()
        # self.fillTable()  # !!!
        self.createModel()
        self.initUI()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        btnAdd = QtWidgets.QPushButton("&Добавить запись")
        btnAdd.clicked.connect(self.addRecord)
        btnDel = QtWidgets.QPushButton("&Удалить запись")
        btnDel.clicked.connect(self.delRecord)

        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)
        layout.addWidget(btnAdd)
        layout.addWidget(btnDel)

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("test_1318914.db")  # !!! .db
        if not self.db.open():
            print("Cannot establish a database connection")
            return False

    def fillTable(self):
        self.db.transaction()
        q = QtSql.QSqlQuery()
        #                             vvvvvvvv
        q.exec_("DROP TABLE IF EXISTS category;")
        q.exec_("CREATE TABLE category (id INT PRIMARY KEY, catname TEXT);")
        q.exec_("INSERT INTO category VALUES (1, 'Расходники');")
        q.exec_("INSERT INTO category VALUES (2, 'Носители');")

        #                             vvvv
        q.exec_("DROP TABLE IF EXISTS good;")
        q.exec_("CREATE TABLE good (Name TEXT, Quantity INT, Category INT);")
        q.exec_("INSERT INTO good VALUES ('Барабан для принтера', 8, 1);")
        q.exec_("INSERT INTO good VALUES ('Бумага для принтера', 3, 1);")
        q.exec_("INSERT INTO good VALUES ('Дискета', 10, 2);")
        self.db.commit()

    def createModel(self):
        self.model = QtSql.QSqlRelationalTableModel()
        self.model.setTable("good")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Название")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Кол-во")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Категория")
        self.set_relation()
        self.model.select()

    def initUI(self):
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        self.view.setColumnWidth(0, 150)
        mode = QtWidgets.QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)

    def closeEvent(self, event):
        if (self.db.open()):
            self.db.close()

    def set_relation(self):
        self.model.setRelation(2, QtSql.QSqlRelation(
            "category",
            "id",
            "catname"
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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Example()
    w.setWindowTitle("QRelationalSqlTableModel")
    w.resize(430, 250)
    w.show()
    app.exec_()