import sys

from PySide2 import QtSql, QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlRelationalTableModel


class RelationalTableModelWithIcon(QSqlRelationalTableModel):
    def __init__(self, state="company", **kwargs):
        self.state = state
        QSqlRelationalTableModel.__init__(self, **kwargs)

    def setState(self, state):
        self.state = state
        # Теперь надо сообщить  в отображение (или другим слушателям), что модель обновилась
        # получаем QModelIndex начала и конца интервала обновления
        # в вашем случае это какой-то столбец
        print(self.index)
        i_start = self.index(0,1)
        i_end   = self.index(self.rowCount() -1, 2)
        self.dataChanged.emit(i_start, i_end)

    def data(self, index, role=Qt.DisplayRole):
        if self.state == "company":
            if index.column() == 1 and role == Qt.DisplayRole:
                return ""
            if index.column() == 1 and role == Qt.DecorationRole:
                return QtGui.QIcon('info.png')
        else:
            if index.column() == 2 and role == Qt.DisplayRole:
                return ""
            if index.column() == 2 and role == Qt.DecorationRole:
                return QtGui.QIcon('info.png')
        return QSqlRelationalTableModel.data(self, index,role)


class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.state = "company"
        self.createConnection()
        self.fillTable()
        self.createModel()
        self.initUI()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.btn_state = QtWidgets.QPushButton("Сменить состояние")
        self.btn_state.clicked.connect(self.state_replace)
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)
        layout.addWidget(self.btn_state)

        if not parent:
            self.show()

    def state_replace(self):
        if self.state == "company":
            self.state = "else"
        else:
            self.state = "company"
        print(self.state)
        self.model.setState(self.state)

    def createConnection(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("local_base.db")
        if not self.db.open():
            print("Cannot establish a database connection")
            return False

    def fillTable(self):
        """
        Вспомогательная функция заполнениия базы данных
        Отключить после тестового запуска
        """

        self.db.transaction()
        q = QtSql.QSqlQuery()
        #
        q.exec_("DROP TABLE IF EXISTS company;")
        q.exec_("CREATE TABLE company ("
                "id INT PRIMARY KEY, "
                "name_company TEXT NOT NULL, "
                "blob_data BLOB NOT NULL );")

        # Вставка тестовых значений
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, blob_data) "
                      "VALUES (:id, :name_company, :blob_data)")

        query.bindValue(":id", 1)
        query.bindValue(":name_company", 'АО КОПЫТА')
        query.bindValue(":blob_data", 'Документы')
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, blob_data) "
                      "VALUES (:id, :name_company, :blob_data)")

        query.bindValue(":id", 2)
        query.bindValue(":name_company", 'АО РОГА')
        query.bindValue(":blob_data", 'Документы')
        query.exec_()

        self.db.commit()

    def createModel(self):
        """
        Создание модели для отображения
        """
        self.model = RelationalTableModelWithIcon(db=self.db, state = self.state)
        self.model.setTable("company")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Документы")
        self.model.select()

    def initUI(self):
        self.view = QtWidgets.QTableView()
        self.view.setModel(self.model)
        mode = QtWidgets.QAbstractItemView.SingleSelection
        self.view.setSelectionMode(mode)

    def closeEvent(self, event):
        if (self.db.open()):
            self.db.close()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    w = Storage_app()
    app.exec_()

