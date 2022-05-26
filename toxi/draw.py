from PySide2 import QtGui

app = QtGui.QGuiApplication([])
# Положим одну картинку на другую
pixmap_map = QtGui.QPixmap('map.jpg')
painter = QtGui.QPainter(pixmap_map)
painter.begin(pixmap_map)
painter.setOpacity(0.5)
painter.drawPixmap(0, 0, QtGui.QPixmap('res.jpg'))
painter.end()
pixmap_map.save('map_plus_res.jpg')