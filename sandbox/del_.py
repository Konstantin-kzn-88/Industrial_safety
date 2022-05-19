import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Model Example'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 240
        self.initUI()

    def initUI(self):

        self.model = QStandardItemModel(0, 0)
        all_items = QStandardItem("Все объекты")
        self.model.appendRow(all_items)
        self.object1 = QStandardItem("Объект 1")
        all_items.appendRow(self.object1)
        self.object2 = QStandardItem("Объект 2")
        all_items.appendRow(self.object2)

        self.view = QTreeView()
        self.view.header().hide()
        self.view.setModel(self.model)

        self.comboBox = QComboBox()
        self.comboBox.addItem("Объект 1")
        self.comboBox.addItem("Объект 2")
        but = QPushButton('Добавить в  группу')
        but.clicked.connect(self.on_click)
        but_rem = QPushButton('Удалить точку')
        but_rem.clicked.connect(self.remove_point)

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.view)
        partLayout = QVBoxLayout()
        partLayout.addWidget(self.comboBox)
        partLayout.addWidget(but)
        partLayout.addWidget(but_rem)
        mainLayout.addLayout(partLayout)

        self.setLayout(mainLayout)

        self.show()

    def on_click(self):
        ind = self.comboBox.currentIndex()
        if ind == 0:
            item = QStandardItem(f'Точка {self.object1.rowCount() + 1}')
            self.object1.setChild(self.object1.rowCount(), item)
        if ind == 1:
            item = QStandardItem(f'Точка {self.object2.rowCount() + 1}')
            self.object2.setChild(self.object2.rowCount(), item)

    def remove_point(self, event):
        index = self.view.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        if not item.parent() is None and item.parent().text().startswith('Объект'):
            item.parent().removeRow(item.row())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())