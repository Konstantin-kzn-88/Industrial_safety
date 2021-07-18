#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from PySide2.QtWidgets import (QWidget, QPushButton, QFrame,
    QColorDialog, QApplication)
from PySide2.QtGui import QColor
from PySide2.QtCore import QTranslator, QLocale
I18N_QT_PATH = str(os.path.join(os.path.abspath('.'), 'i18n'))


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        col = QColor(0, 0, 0)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)

        self.btn.clicked.connect(self.showDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())
        self.frm.setGeometry(130, 22, 100, 100)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Color dialog')
        self.show()


    def showDialog(self):

        col = QColorDialog.getColor()
        print(col)

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    locale = 'ru_RU'
    qt_translator = QTranslator(app)
    qt_translator.load('{}/qtbase_{}.qm'.format(I18N_QT_PATH, locale))
    app_translator = QTranslator(app)
    app_translator.load('{}/{}.qm'.format(I18N_QT_PATH, locale))
    app.installTranslator(qt_translator)
    app.installTranslator(app_translator)
    ex = Example()
    app.exec_()