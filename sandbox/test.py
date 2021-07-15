from PySide2.QtWidgets import *
import sys

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        label1 = QLabel("Индекс вкладки 0.")
        label2 = QLabel("Индекс вкладки 1.")
        tabwidget = QTabWidget()
        tabwidget.blockSignals(True)
        tabwidget.currentChanged.connect(self.onChange)
        tabwidget.addTab(label1, "Tab 0")
        tabwidget.addTab(label2, "Tab 1")
        layout.addWidget(tabwidget, 0, 0)
        tabwidget.blockSignals(False)

    def onChange(self,i):
        print(f"Индекс вкладки {i}")
        if i == 0:
            print("То что должно быть в функции 1")
        else:
            print("То что должно быть в функции 2")

app = QApplication(sys.argv)
screen = Window()
screen.show()
app.exec_()