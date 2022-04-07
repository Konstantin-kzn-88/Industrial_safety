from PySide2 import QtWidgets, QtGui, QtCore
import sqlite3 as sql
import os
from pathlib import Path



class Data_base(QtWidgets.QWidget):
    def __init__(self, db_name: str, db_path: str):
        super().__init__()
        self.db_name = db_name
        self.db_path = db_path

        path_ico = str(Path(os.getcwd()).parents[0])
        main_ico = QtGui.QIcon(path_ico + '/ico/comp.png')
        self.setWindowIcon(main_ico)

    def db_create(self) -> tuple:
        """
        Создание новой БД
        """
        # 1. Получить имя новой базы данных
        text, ok = QtWidgets.QInputDialog.getText(self, 'Создать новую базу данных', 'Введите имя новой базы данных:')

        if len(text) == 0 and ok:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("База данных не может быть с пустым названием!")
            msg.exec()
            return ('', '')
        elif ok == False:
            return ('', '')

        # 2. Проверить нет ли базы данных с этим же именем по тому же пути
        dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Выбрать путь базы данных",
                                                         str(Path(os.getcwd()))[:3],
                                                         QtWidgets.QFileDialog.ShowDirsOnly
                                                         | QtWidgets.QFileDialog.DontResolveSymlinks)

        check = os.path.exists(f"{dir}/{text}.db")

        if check:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("База данных с таким названием уже существует!")
            msg.exec()
            return ('', '')
        # 3. Запишем путь и имя БД в переменную
        self.db_name = f'{text}.db'
        self.db_path = dir
        # 4. Создадим базу данных
        with sql.connect(f'{dir}/{text}.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""CREATE TABLE objects(id INTEGER PRIMARY KEY, data TEXT NOT NULL,
                                                    plan BLOB NOT NULL, name_plan TEXT NOT NULL)""")

        return (self.db_name, self.db_path)

    def db_connect(self) -> tuple:
        """
        Подключение к существующей БД
        """

        path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть базу данных',
                                                     str(Path(os.getcwd()))[:3], ("Data base (*.db)"))[0]
        if path == "":
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Файл базы данных не выбран")
            msg.exec()
            return ('', '')
        file_name = QtCore.QFileInfo(path).fileName()
        file_path = QtCore.QFileInfo(path).path()
        self.db_name = file_name
        self.db_path = file_path

        return (self.db_name, self.db_path)

    def plan_add(self):
        """
         Загрузка файла картинки в базу данных
        """
        # Проверка подключения к базе данных
        # проверка базы данных
        if self.db_path != '' and self.db_name != '':

            file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть генеральный план',
                                                              str(Path(os.getcwd()))[:3], ("Images (*.jpg)"))[0]
            file_name = QtCore.QFileInfo(file_path).fileName()
            # Проверка выбран ли файл ген.плана
            if file_path == "":
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText("Файл не выбран")
                msg.exec()
                return


            # Подключение к базе данных
            path_str = f'{self.db_path}/{self.db_name}'.replace("/", "//")

            with sql.connect(path_str) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM objects")
                real_id = cursor.fetchall()
                print()
                # проверка максимального id в базе
                max_id = 1 if real_id == [] else max(real_id)[0] + 1
                # SQL запрос на вставку BLOB
                sqlite_insert_blob_query = """ INSERT INTO 'objects'
                                                    ('id', 'data', 'plan', 'name_plan') VALUES (?, ?, ?, ?)"""
                # Конвертация файла в BLOB
                plan_to_blob = self.convertToBinaryData(file_path)
                # Проготовим множество к вставке в SQL запрос
                data_tuple = (max_id, "", plan_to_blob, file_name)
                cursor.execute(sqlite_insert_blob_query, data_tuple)

        else:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("База данных не подключена!")
            msg.exec()
            return

    def convertToBinaryData(self, file_path):
        # Конвертирование в BLOB
        with open(file_path, 'rb') as file:
            blobData = file.read()
        return blobData

    def plan_list_update(self, plan_list):
        """
        Обновление списка ген.планов при:
        - подключении БД
        - добавлении ген.плана
        - удалении ген.плана

        :param -plan_list type (QtWidgets.QComboBox)
        """
        if self.db_path != '' and self.db_name != '':
            path_str = f'{self.db_path}/{self.db_name}'.replace("/", "//")

            with sql.connect(path_str) as connection:

                cursor = connection.cursor()
                cursor.execute("SELECT id, name_plan FROM objects")
                plan_in_db = cursor.fetchall()

                # Очистить QtWidgets.QComboBox
                plan_list.clear()

                plan_item = []

                for row in plan_in_db:
                    name_plan = str(f'{row[0]}, {row[1]}')
                    plan_item.append(name_plan)
                if plan_item == []:
                    plan_list.addItems(["--Нет ген.планов-- "])
                else:
                    plan_list.addItems(plan_item)


    def get_plan_in_db(self, text: str):
        """
        Функция получения картинки из базы данных
        :param text - строка полученная из QComboBox (id и name_plan)
        :return image_data - BLOB формат картинки или None если картинка в базе не найдена
        """
        if self.db_path != '' and self.db_name != '':
            path_str = f'{self.db_path}/{self.db_name}'.replace("/", "//")

            with sql.connect(path_str) as connection:

                cursor = connection.cursor()
                cursor.execute("SELECT * FROM objects")
                plan_in_db = cursor.fetchall()
                for row in plan_in_db:
                    if str(f'{row[0]}, {row[3]}') == text:
                        image_data = row[2]
                        return image_data
                return



