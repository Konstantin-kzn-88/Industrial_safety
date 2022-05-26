import sys

from PySide2 import QtGui
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


def set_pix_color(qimg_zone, max_el, value, x ,y):

    if x ==0 or y == 0:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 0, 0, 255))

    if value >= max_el:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 0, 0, 255))
    #     красный
    elif max_el * 1.00 > value >= max_el * 0.003:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 10, 0, 255))
    # рыжий
    elif max_el * 0.003 > value >= max_el * 0.001:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 40, 0, 255))

    # желтый
    elif max_el * 0.001 > value >= max_el * 0.00005:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 170, 0, 255))

    # салатовый
    elif max_el * 0.00005 > value >= max_el * 0.000005:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(230, 255, 0, 255))

    # зеленый
    elif max_el * 0.000005 > value >= max_el * 0.0000005:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(100, 255, 0, 255))

    # голубой
    elif max_el * 0.0000005 > value >= max_el * 0.00000005:
        qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 255, 40, 255))


    # # темно-голубой
    # elif max_el * 0.01 > value >= max_el * 0.009:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 220, 255, 255))
    # elif max_el * 0.009 > value >= max_el * 0.008:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 210, 255, 255))
    # elif max_el * 0.008 > value >= max_el * 0.007:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 200, 255, 255))
    # elif max_el * 0.007 > value >= max_el * 0.006:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 190, 255, 255))
    # elif max_el * 0.006 > value >= max_el * 0.005:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 160, 255, 255))
    # elif max_el * 0.005 > value >= max_el * 0.004:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 150, 255, 255))
    # #     синий
    # elif max_el * 0.004 > value >= max_el * 0.003:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 130, 255, 255))
    # elif max_el * 0.003 > value >= max_el * 0.0025:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 110, 255, 255))
    # elif max_el * 0.0025 > value >= max_el * 0.0015:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 90, 255, 255))
    # elif max_el * 0.0015 > value >= max_el * 0.001:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 70, 255, 255))
    # elif max_el * 0.001 > value >= max_el * 0.0008:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 50, 255, 255))
    # elif max_el * 0.0008 > value >= max_el * 0.0007:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 40, 255, 255))
    # elif max_el * 0.0007 > value >= max_el * 0.0006:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 30, 255, 255))
    # elif max_el * 0.0006 > value >= max_el * 0.0002:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 20, 255, 255))
    # elif max_el * 0.0002 > value >= max_el * 0.0001:
    #     qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 0, 255, 255))

def get_max_elem(data:list):
    max_elem = 0
    for list_ in data:
        i = max(list_)
        if i>max_elem:
            max_elem = i
    print(max_elem)
    return max_elem


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



app = QtGui.QGuiApplication([])
pixmap = QtGui.QPixmap(row[0], col[1])
pixmap.fill(QtGui.QColor(255, 255, 255, 255))
image_zone = pixmap.toImage()  #

max_elem = get_max_elem(val)

for row in range(0, col[1]-1):
    for iter in range(0, len(val[row])-1):
        set_pix_color(image_zone, max_elem, val[row][iter], iter, row)

image_zone.save('res.jpg')

# Положим одну картинку на другую
pixmap_map = QtGui.QPixmap('map.jpg')
painter = QtGui.QPainter(pixmap_map)
painter.begin(pixmap_map)
painter.setOpacity(0.5)
painter.drawPixmap(0, 0, QtGui.QPixmap('res.jpg'))
painter.end()
pixmap_map.save('map_plus_res.jpg')
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
