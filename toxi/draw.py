from PySide2 import QtGui


app = QtGui.QGuiApplication([])
# Положим одну картинку на другую
pixmap_map = QtGui.QPixmap('map.jpg')
pixmap_zone = QtGui.QPixmap('res.jpg')
pixmap_zone = pixmap_zone.scaled(300, 300)


t = QtGui.QTransform().rotate(35)

painter = QtGui.QPainter(pixmap_map)
painter.begin(pixmap_map)
painter.setOpacity(0.5)
painter.drawPixmap(150, 150, pixmap_zone.transformed(t))
painter.end()
pixmap_map.save('map_plus_res.jpg')