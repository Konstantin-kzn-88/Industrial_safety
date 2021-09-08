
import sys
import os
from pathlib import Path

from PySide2 import QtSql, QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtSql import QSqlRelationalTableModel


class RelationalTableModelWithIcon(QSqlRelationalTableModel):

    def data(self, index, role=Qt.DisplayRole): # Переопределяем метод data
        if index.column() == 2 and role == Qt.DisplayRole: # для второго столбца, скроем выводимый текст
            return ""
        if index.column() == 2 and role == Qt.DecorationRole: # и для него же выведем иконку в качестве декора
            return QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/company.png')
        return QSqlRelationalTableModel.data(self,index, role) # все остальное должно штатно обработаться qsqltablemodel




class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.createConnection()
        self.fillTable()  # !!! тестовое заполнение базы данных
        self.createModel()
        self.initUI()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)

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
                "blob_data BLOB NOT NULL );")

        # Вставка тестовых значений
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, blob_data) "
                      "VALUES (:id, :name_company, :blob_data)")

        query.bindValue(":id", 1)
        query.bindValue(":name_company", 'АО КОПЫТА')
        query.bindValue(":blob_data", test_BLOB)
        query.exec_()

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO company (id, name_company, blob_data) "
                      "VALUES (:id, :name_company, :blob_data)")

        query.bindValue(":id", 2)
        query.bindValue(":name_company", 'АО РОГА')
        query.bindValue(":blob_data", test_BLOB)
        query.exec_()

        self.db.commit()

    def createModel(self):
        """
        Создание модели для отображения
        """
        self.model = RelationalTableModelWithIcon(db = self.db)
        self.model.setTable("company")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Наиманование")
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