# -----------------------------------------------------------
# Класс предназначен для построения общего GUI-калькуляторов
# На основе списка создаются:
# 1. Поля для ввода объектов QDoubleSpinBox
# и панель управления:
# 2. QRadioButton выбора построения графика/записи в excel
# 3. Кпопка расчета
# Т.е. характерный вид для многих калькуляторов:
# числовые значения -> выбор график/запись -> кнопка расчета
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import traceback
from excel import class_xl_report

class Minimal_GUI(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None, columns= [])-> None:

        QtWidgets.QWidget.__init__(self, parent)
        self.columns = columns
        # откроем Excel
        self.Excel = class_xl_report.Excel()
        self.Excel.create(self.columns)
        # GUI
        layout = QtWidgets.QFormLayout(self)
        # создадим список на уровне конструктора
        # что бы засунуть в него QDoubleSpinBox
        # для принятия значений
        self.form_elem = [None for i in range(len(self.columns))]
        for name in self.columns:
            # Создадим в цикле QDoubleSpinBox по размерности
            # переданного списка для принятия от пользователя значений
            spin = QtWidgets.QDoubleSpinBox(self)
            spin.setObjectName('spin' + str(self.columns.index(name)))
            spin.setDecimals(2)
            spin.setRange(0, 100000)
            spin.setSingleStep(0.01)
            spin.setSuffix("    " + name)
            line = spin.lineEdit()
            line.setFont(QtGui.QFont("Times", 8, QtGui.QFont.Bold))
            layout.addRow(spin)
            self.form_elem[self.columns.index(name)] = spin

        #  создаем радио кнопки для выбора действия
        self.write_excel = QtWidgets.QRadioButton('Записать в Excel')
        self.write_excel.setChecked(True)
        self.plot_graph = QtWidgets.QRadioButton('Построить график')
        # создаем кнопку расчета которая на основе радио кнопок
        # произведет нужный расчет или построит график
        self.btn_calc = QtWidgets.QPushButton("Расчет")
        layout.addRow(self.write_excel)
        layout.addRow(self.plot_graph)
        layout.addRow(self.btn_calc)

        layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        if not parent:
            self.show()

    def get_form_val(self) -> list:
        # функция для считывания значений QDoubleSpinBox
        # созданных в цикле на уровне конструктора
        res = []
        for form_val in self.form_elem:
            print(form_val.value())
            res.append(form_val.value())
        return res

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        messageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Question,
            "Выход из программы",
            "Выйти из программы?",
            (QtWidgets.QMessageBox.Yes
             | QtWidgets.QMessageBox.No)
        )
        resultCode = messageBox.exec_()
        if resultCode == QtWidgets.QMessageBox.No:
            return event.ignore()
        elif resultCode == QtWidgets.QMessageBox.Yes:
            self.Excel.close()
            return QtWidgets.QWidget.closeEvent(self, event)


def log_uncaught_exceptions(ex_cls, ex, tb):
    # pyqt визуализация ошибок
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    QtWidgets.QMessageBox.critical(None, 'Error', text)
    sys.exit()

sys.excepthook = log_uncaught_exceptions

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Minimal_GUI()
    app.exec_()
