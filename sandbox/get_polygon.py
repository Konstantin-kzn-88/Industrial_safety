from PySide2 import QtGui, QtCore

coordinate = ["699.0", "608.0", "724.0", "584.0", "718.0", "535.0", "712.0", "460.0", "712.0", "404.0", "722.0", "361.0",
       "708.0", "320.0", "693.0", "280.0", "677.0", "236.0", "669.0", "191.0", "660.0", "163.0", "643.0", "122.0",
       "589.0", "116.0", "546.0", "115.0", "478.0", "125.0", "476.0", "164.0", "490.0", "209.0"]

def get_polygon(coordinate):
    i = 0
    points = []
    while i < len(coordinate):
        point = QtCore.QPoint(int(float(coordinate[i])), int(float(coordinate[i + 1])))
        points.append(point)
        i += 2
    polygon = QtGui.QPolygon(points)

    return polygon


if __name__ == '__main__':
    polygon = get_polygon(coordinate)
    print(polygon)
