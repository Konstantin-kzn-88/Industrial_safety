from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtGui import QPen,QPainter, QPolygon, QRadialGradient, QBrush, QColor
from PyQt5.QtCore import QPoint, Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Drawing Polygon"
        self.width = 900
        self.height = 900
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0,0, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QRadialGradient(50, 50, 50, 50, 50)
        gradient.setColorAt(0, QColor.fromRgbF(100, 125, 0, 0.5))
        gradient.setColorAt(1, QColor.fromRgbF(0, 255, 0, 0.5))
        brush = QBrush(gradient)
        pen = QPen(brush, 50, Qt.SolidLine)
        pen.setJoinStyle(Qt.RoundJoin)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        points = QPolygon([
            QPoint(80,80),
            QPoint(80,500),
            QPoint(500,80),
            QPoint(500,500)
        ])

        painter.drawPolyline(points)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())