import re
import sys
from PyQt5 import QtSql
from PyQt5.Qt import *

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.createConnection()
        self.fillTable()  # !!!
        self.createModel()
        self.initUI()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.table_box = QComboBox()
        self.table_box.addItems(["Оборудование", "Категории"])
        self.table_box.activated[str].connect(self.table_select)
        search_str = QLineEdit()
        search_str.setPlaceholderText("Введите строку поиска")
        search_str.textChanged.connect(self.update_filter)

        layout = QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)
        layout.addWidget(self.table_box)
        layout.addWidget(search_str)

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
        q.exec_("DROP TABLE IF EXISTS equipment;")
        q.exec_("CREATE TABLE equipment (Name TEXT, Quantity INT, Category INT);")
        q.exec_("INSERT INTO equipment VALUES ('Барабан для принтера', 8, 1);")
        q.exec_("INSERT INTO equipment VALUES ('Бумага для принтера', 3, 1);")
        q.exec_("INSERT INTO equipment VALUES ('Дискета', 10, 2);")
        self.db.commit()

    def createModel(self):
        self.model = QtSql.QSqlRelationalTableModel()
        self.model.setTable("equipment")
        self.model.select()

    def initUI(self):
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setColumnWidth(0, 150)
        mode = QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)


    def update_filter(self, text):
        if self.table_box.currentText() == 'Категории':
            s = re.sub("[\W_]+", "", text)
            filter_str = 'catname LIKE "%{}%"'.format(s)
            self.model.setFilter(filter_str)
        elif self.table_box.currentText() == 'Оборудование':
            s = re.sub("[\W_]+", "", text)
            filter_str = 'Name LIKE "%{}%"'.format(s)
            self.model.setFilter(filter_str)

    def table_select(self, text):
        if text == 'Категории':
            self.model.setTable("category")
            self.model.select()
        elif text == 'Оборудование':
            self.model.setTable("equipment")
            self.model.select()

    def closeEvent(self, event):
        if (self.db.open()):
            self.db.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Example()
    w.setWindowTitle("Search")
    w.resize(430, 250)
    w.show()
    sys.exit(app.exec_())