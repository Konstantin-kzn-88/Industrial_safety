from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QTableView
from PyQt5.QtCore import QSize, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel


# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)

        self.row_now_select = None

        self.setMinimumSize(QSize(480, 80))  # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")  # Устанавливаем заголовок окна
        central_widget = QWidget(self)  # Создаём центральный виджет
        self.setCentralWidget(central_widget)  # Устанавливаем центральный виджет

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.model_data = QStandardItemModel(5, 32)
        self.table_view = QTableView()
        self.table_view.setModel(self.model_data)
        self.table_view.clicked[QModelIndex].connect(self.clicked)

        okButton = QPushButton("OK")
        okButton.clicked.connect(self.func_0)
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(self.func_1)

        grid_layout.addWidget(self.table_view, 0, 0)  # Добавляем таблицу в сетку
        grid_layout.addWidget(okButton, 1, 0)
        grid_layout.addWidget(cancelButton, 2, 0)

        self.show()

    def func_1(self):
        pass
        # Удалить выбранную строку
        # if self.row_now_select == None:
        #     return
        # self.model_data.removeRow(self.row_now_select)
        # self.row_now_select = None

    def func_0(self):
        pass

    def clicked(self, index):
        item = self.model_data.itemFromIndex(index)
        print(item.index().column(), item.index().row())  # получить строку, столбец по индексу

        self.row_now_select = item.index().row()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
