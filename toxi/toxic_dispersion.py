import sys
from PySide2.QtWidgets import (QWidget, QHBoxLayout,
                               QLabel, QApplication, QMessageBox)
from PySide2.QtGui import QPixmap, QImage, QPainter, QGuiApplication, QColor
import traceback
from pathlib import Path
import xlwings as xw


def get_row_col_index(sheet):
    row = 0
    col = 0
    # find col
    for i in range(1, 5000):
        val = sheet.range((1, i)).value
        if val == None:
            col = (1, i - 1)
            break
    # find row
    for i in range(1, 5000):
        val = sheet.range((i, 1)).value
        if val == None:
            row = (i - 1, 1)
            break

    return row, col


def get_data_in_excel(row: tuple, col: tuple) -> list:
    return sheet.range((2, 2), (row[0], col[1])).options(
        ndim=2).value  # с 2 - т.к. нужно ислючить размерность длины по X, Y


DATA_PATH = Path.cwd()
SCALE = 1.443  # т.е. в 1 метре 1.443 пикселя

print(f'{DATA_PATH}//data25.xls')
wb = xw.Book(f'{DATA_PATH}//data25.xls')
sheet = wb.sheets['Лист1']

row, col = get_row_col_index(sheet)
if row != 0 and col != 0:
    val = get_data_in_excel(row, col)
else:
    val = 0

print(row, col)

app = QGuiApplication([])
pixmap = QPixmap(row[0], col[1])
pixmap.fill(QColor(255, 255, 255, 255))
image_zone = pixmap.toImage()  #

print(row[0], col[1])

for i in range(0, col[1]-1):

    for j in val[i]:

        if val[i][val[i].index(j)] > 0:
            image_zone.setPixelColor(j, i, QColor(0, 0, 255, 255))

image_zone.save('cat.jpg')



# pixmap_zone = QPixmap(map.width(), map.height())
# # Создадим QPainter
# qp = QPainter(pixmap_zone)
# # Начнем рисование
# qp.begin(pixmap_zone)


# print(val)


#
# class Example(QWidget):
#
#     def __init__(self, scale=8, pos_x=500, pos_y=500):
#         super().__init__()
#         self.scale = scale
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.initUI()
#
#     def initUI(self):
#         # Рисование данных
#         # 1. Получим на основе копии картинки основу для рисования
#         map = QPixmap("map.jpg")
#         pixmap_zone = QPixmap(map.width(), map.height())
#         pixmap_zone.fill(QColor(255, 255, 255, 255))
#
#         # Создадим QPainter
#         qp = QPainter(pixmap_zone)
#         # Начнем рисование
#         qp.begin(pixmap_zone)
#
#         hbox = QHBoxLayout(self)
#         pixmap = QPixmap.fromImage(image)
#
#         lbl = QLabel(self)
#         lbl.setPixmap(pixmap)
#
#         hbox.addWidget(lbl)
#         self.setLayout(hbox)
#
#         self.move(300, 200)
#         self.setWindowTitle('Toxi')
#         self.show()
#
#
# def log_uncaught_exceptions(ex_cls, ex, tb):
#     # pyqt визуализация ошибок
#     text = '{}: {}:\n'.format(ex_cls.__name__, ex)
#     text += ''.join(traceback.format_tb(tb))
#     print(text)
#     QMessageBox.critical(None, 'Error', text)
#     sys.exit()
#
#
# sys.excepthook = log_uncaught_exceptions
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main = Example()
