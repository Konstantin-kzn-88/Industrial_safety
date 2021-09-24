import sys
import os
from PyQt5 import QtSql
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class Storage_app(QtWidgets.QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.createConnection()
        self.fillTable()  # !!! тестовое заполнение базы данных
        self.createModel()
        self.initUI()

        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        btn_save = QtWidgets.QPushButton("Скачать файл из БД")
        btn_save.clicked.connect(self.save_file)
        layout = QtWidgets.QVBoxLayout(self.centralWidget)
        layout.addWidget(self.view)
        layout.addWidget(btn_save)

        if not parent:
            self.show()

    def save_file(self):
        print("Как сохранить этот файл из базы данных? =(")
        #
        # list_id = []
        # max_id = 0
        # if self.model.rowCount() == 0:
        #     max_id = max_id + 1
        # else:
        #     for row in range(self.model.rowCount()):
        #         for column in range(self.model.columnCount()):
        #             if column != 2:
        #                 index = self.model.index(row, column)
        #                 list_id.append(index.data())
        #     print(list_id)
        selected_indexes = self.view.selectedIndexes()
        if not selected_indexes:
            return
        index = selected_indexes[0]
        row = selected_indexes[0].row()
        column = selected_indexes[0].column()
        print(f'selected_indexes = {row} - {column}')
        if column != 2:
            return

        r = self.model.record(row)
        blob_data = r.value(column)
        print(f'blob_data = {type(blob_data)}')  # QtCore.QByteArray
        outputfilename = f'test_{row}_{column}.pdf'
        with open(outputfilename, 'wb') as output:
            output.write(blob_data)

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
        file_path = (f"{os.getcwd()}\\test_BLOB.pdf")
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
        self.model = QtSql.QSqlRelationalTableModel()
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

def my_excepthook(type, value, tback):
   #  функция отлова ошибок на PyQt5
   QtWidgets.QMessageBox.critical(
       window, "CRITICAL ERROR", str(value),
       QtWidgets.QMessageBox.Cancel
   )

   sys.__excepthook__(type, value, tback)


sys.excepthook = my_excepthook

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    w = Storage_app()
    app.exec_()