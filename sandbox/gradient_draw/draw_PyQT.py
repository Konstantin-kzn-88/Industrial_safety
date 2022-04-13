from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPen, QPainter, QPolygon, QRadialGradient, QBrush, QColor
from PyQt5.QtCore import QPoint, Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Polygon"
        self.width = 900
        self.height = 900
        self.InitWindow()

        self.points = QPolygon([
            QPoint(80, 80),
            QPoint(80, 500),
            QPoint(500, 80),
            QPoint(500, 500)
        ])

        self.max_zone = 200
        self.colors_range = [i for i in range(255, 0, -1)]

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        i = 0
        for radius in range(self.max_zone, 1, -1):
            brush = QBrush(QColor(255, self.colors_range[i], 0))
            pen = QPen(brush, radius, Qt.SolidLine)
            pen.setJoinStyle(Qt.RoundJoin)
            pen.setCapStyle(Qt.RoundCap)
            painter.setPen(pen)
            painter.drawPolyline(self.points)
            i += 1


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
