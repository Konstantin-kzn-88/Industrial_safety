import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex


class Table(QWidget):
    def __init__(self):
        super(Table, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Пример QTableWidget')
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.TableWidget = QTableWidget(1, 3)

        # Заголовки.
        self.TableWidget.setHorizontalHeaderLabels(['Поз.', 'Объем, м3', 'Расположение'])

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_button_func)
        del_button = QPushButton("Del")
        del_button.clicked.connect(self.del_button_func)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_button_func)

        # self.TableWidget.itemSelectionChanged.connect(self.save_button_func)
        self.TableWidget.clicked[QModelIndex].connect(self.clicked)

        # Добавить данные
        newItem = QTableWidgetItem('Чжан Сан')

        self.TableWidget.setItem(0, 0, newItem)

        newItem = QTableWidgetItem('Male')


        self.TableWidget.setItem(0, 1, newItem)

        newItem = QTableWidgetItem('160')
        self.TableWidget.setItem(0, 2, newItem)

        layout.addWidget(self.TableWidget)
        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def del_button_func(self):
        index = self.TableWidget.currentIndex()
        print(index.row())
        self.TableWidget.removeRow(index.row())

    def add_button_func(self):
        value = self.TableWidget.rowCount()
        print(value)
        self.TableWidget.insertRow(value)

    def save_button_func(self):
        print("save")

    def clicked(self, index):
        print(index.row())
        # item = self.TableWidget.itemFromIndex(index)
        # print(item)
        # print(item.column(), item.row())  # получить столбец/строку   по индексу

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Table()
    win.show()
    sys.exit(app.exec())
