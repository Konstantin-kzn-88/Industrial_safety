from PySide2 import QtSql, QtCore
import os

def convertToBinaryData(file_path):
    # Конвертирование в BLOB
    with open(file_path, 'rb') as file:
        blobData = file.read()
        print()
    return blobData


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("local_base.db")  # !!! .db
    if not db.open():
        print("Cannot establish a database connection")
        return False
    return db

# Получим данные BLOB
# картинка test_BLOB.jpg рядом с файлом скрипта
file_path = (f"{os.getcwd()}\\test_BLOB.jpg")
test_BLOB = convertToBinaryData(file_path)
ba = QtCore.QByteArray(test_BLOB)

db = createConnection()
db.transaction()
q = QtSql.QSqlQuery()
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
query.bindValue(":blob_data", ba)
query.exec_()

db.commit()


if __name__ == '__main__':
    print("Запуск")
