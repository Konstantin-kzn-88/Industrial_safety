from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QTableView, QMessageBox
from PyQt5.QtCore import QSize, Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem


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

        self.model_data = QStandardItemModel(2, 5)
        self.table_view = QTableView()
        self.table_view.setModel(self.model_data)
        self.table_view.clicked[QModelIndex].connect(self.clicked)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_button_func)
        del_button = QPushButton("Del")
        del_button.clicked.connect(self.del_button_func)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_button_func)

        grid_layout.addWidget(self.table_view, 0, 0)  # Добавляем таблицу в сетку
        grid_layout.addWidget(add_button, 1, 0)
        grid_layout.addWidget(del_button, 2, 0)
        grid_layout.addWidget(save_button, 3, 0)

        self.show()

    def save_button_func(self):
        if self.row_now_select == None:
            return

        data_list = []
        quantity_row = self.model_data.rowCount()  # общее количество строк

        try:
            for row in range(0,quantity_row):
                row_list = []
                for item in range(0,5):
                    add = self.model_data.item(row, item).text()
                    row_list.append(add)
                data_list.append(row_list)
            print(data_list)
        except:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText("Не все данные заполнены")
            msg.exec()
            return



    def del_button_func(self):
        # Удалить выбранную строку
        if self.row_now_select == None:
            return
        self.model_data.removeRow(self.row_now_select)
        self.row_now_select = None

    def add_button_func(self):
        self.model_data.appendRow(QStandardItem(1,5))  # добавить строку

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
