# -----------------------------------------------------------
# Графический интерфейс предназначен для отрисовки зон действия
# поражающих факторов и построения полей потенциального риска
# на основе данных из excel (расчеты в данном модуле не производятся)
# приказ мчс №404
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from pathlib import Path
from PySide2 import QtWidgets, QtGui



class Painter(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # Иконки
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/painter.png')
        exit_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/exit.png')
        info_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/info.png')
        # Главное окно
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Painter')
        self.setWindowIcon(self.main_ico)
        # Центральный виджет
        text_edit = QtWidgets.QTextEdit()
        self.setCentralWidget(text_edit)
        # Выход из приложения
        exit_action = QtWidgets.QAction(exit_ico, 'Выход', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Выход из Painter')
        exit_action.triggered.connect(self.close_event)
        # О приложении
        about_action = QtWidgets.QAction(info_ico, 'О приложении', self)
        about_action.setShortcut('F1')
        about_action.setStatusTip('О приложении')
        about_action.triggered.connect(self.about_programm)


        # Меню приложения
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addAction(exit_action)
        file_menu = menubar.addMenu('О приложении')
        file_menu.addAction(about_action)
        # Установить статусбар
        self.statusBar()

        # toolbar = self.addToolBar('Выход')
        # toolbar.addAction(exitAction)


        self.show()

    #     Функция выхода из программы
    def close_event(self) -> None:
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            "Выход из программы",
            "Выйти из программы?",
            (QtWidgets.QMessageBox.Yes
             | QtWidgets.QMessageBox.No)
        )
        messageBox.setButtonText(QtWidgets.QMessageBox.Yes, "Да")
        messageBox.setButtonText(QtWidgets.QMessageBox.No, "Нет")
        messageBox.setWindowIcon(self.main_ico)
        resultCode = messageBox.exec_()
        if resultCode == QtWidgets.QMessageBox.No:
            return
        elif resultCode == QtWidgets.QMessageBox.Yes:
            return self.close()


    #     Функция "О программе"
    def about_programm(self) -> None:
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Information,
            "О программе",
            """Программа <b>Painter</b>. Предназначена для отрисовки зон действия 
поражающих факторов и построения полей потенциального риска 
на основе данных из Excel. Разрабочик: <b>npfgsk.ru</b>""",
            (QtWidgets.QMessageBox.Ok)
        )
        messageBox.setWindowIcon(self.main_ico)
        messageBox.exec_()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Painter()
    app.exec_()