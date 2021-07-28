#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PySide2.QtWidgets import (QWidget, QHBoxLayout,
                               QLabel, QApplication, QMessageBox)
from PySide2.QtGui import QPixmap, QColor, QImage
import traceback


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("cat.jpg")
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_ARGB32)
        for y in range(0, image.height() + 1):
            for x in range(0, image.width() + 1):
                print(image.pixelColor(x, y).getRgbF())
                if image.pixelColor(x, y).getRgbF() == (1.0, 1.0, 1.0, 1.0):
                    image.setPixelColor(x, y, QColor(0, 0, 0, 0))

        pixmap = QPixmap.fromImage(image)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Red Rock')
        self.show()


def log_uncaught_exceptions(ex_cls, ex, tb):
    # pyqt визуализация ошибок
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Example()
    app.exec_()
