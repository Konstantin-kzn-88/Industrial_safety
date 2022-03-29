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

        self.TableWidget = QTableWidget(0, 3)

        # Заголовки.
        self.TableWidget.setHorizontalHeaderLabels(['Поз.', 'Объем, м3', 'Расположение'])

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_button_func)
        del_button = QPushButton("Del")
        del_button.clicked.connect(self.del_button_func)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_button_func)
        append_button = QPushButton("Append")
        append_button.clicked.connect(self.append_button_func)

        # self.TableWidget.itemSelectionChanged.connect(self.save_button_func)
        self.TableWidget.clicked[QModelIndex].connect(self.clicked)

        layout.addWidget(self.TableWidget)
        layout.addWidget(add_button)
        layout.addWidget(del_button)
        layout.addWidget(save_button)
        layout.addWidget(append_button)

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
        data_list = []
        # Записать данные
        count_row = 0 # начинаем с 0 строки

        for _ in range(0, self.TableWidget.rowCount()):  # посчитаем строки
            append_list = [] # заведем пустой список для объекта
            count_col = 0  # колонка с индесом 0
            for _ in range(0, self.TableWidget.columnCount()):  # для каждого столбца строки
                append_list.append(self.TableWidget.item(count_row, count_col).text()) # добавим в словарь текст ячейки
                count_col += 1  # + 1 к столбцу
            data_list.append(append_list) # добавим объект
            count_row += 1  # +1 к строке (новая строка если len(data_list) > 1)
        print(data_list)



    def clicked(self, index):
        print(index.row())
        # item = self.TableWidget.itemFromIndex(index)
        # print(item)
        # print(item.column(), item.row())  # получить столбец/строку   по индексу

    def append_button_func(self):

        data_list = [['T-3', '100', 'Under'], ['T-4', '400', 'On']]
        # Добавить данные
        count_row = self.TableWidget.rowCount()  # посчитаем количество строк

        for item in data_list:  # возьмем каждый словарь из data_list
            count_col = 0  # колонка с индесом 0
            # вставим строку, т.е. если строк 0, то на 0 позицию по индексу,
            # если кол-во строк 1 то на 1 позицию по индексу
            self.TableWidget.insertRow(count_row)
            for var in item:  # для каждого значения из словаря item пробежим по столбцам
                TableWidgetItem = QTableWidgetItem(var)
                self.TableWidget.setItem(count_row, count_col, TableWidgetItem)
                count_col += 1  # + 1 к столбцу
            count_row += 1  # +1 к строке (новая строка если len(data_list) > 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Table()
    win.show()
    sys.exit(app.exec())
