from PySide2 import QtWidgets, QtGui
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
