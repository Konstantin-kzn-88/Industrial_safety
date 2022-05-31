from PySide2 import QtGui
from pathlib import Path
import xlwings as xw
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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

#
cmap = ListedColormap(["white", "blue", "cyan", "lime", "yellow", 'red'])
plt.figure(figsize=(10, 10), dpi=30)
plt.imshow(val, cmap=cmap, interpolation='bicubic', vmax=0.1)
plt.axis('off')
plt.savefig('res.jpg', bbox_inches='tight', pad_inches=0)

app = QtGui.QGuiApplication([])
# Положим одну картинку на другую
pixmap_map = QtGui.QPixmap('map.jpg')
# **************************************
pixmap_zone = QtGui.QPixmap('res.jpg')
# pixmap_zone = pixmap_zone.scaled(300, 300)
t = QtGui.QTransform().rotate(35)
# **************************************
painter = QtGui.QPainter(pixmap_map)
painter.begin(pixmap_map)
painter.setOpacity(0.5)
painter.drawPixmap(50, 50, pixmap_zone.transformed(t))
painter.end()
pixmap_map.save('map_plus_res.jpg')
