# -----------------------------------------------------------
# Графический интерфейс предназначен для расчета огненного шара
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from PySide2 import QtWidgets, QtGui
from pathlib import Path
import traceback
import math

# local import
from event_tree import class_event_tree as et
from calc_gui import class_calc_gui


class Calc_GUI(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.table_header = 0  # установлена ли шабка для талицы
        # Иконка и название
        self.setWindowTitle('Расчет сценариев аварии (Приказ МЧС 404)')
        self.setWindowIcon(QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/calc_ico.png'))
        # списки для таблицы (шапка)
        self.table_header = 0  # установлена ли шабка для талицы
        self.header = ['Температура вспышки, град.С', 'Расход, кг/с', 'Вероятность, число', '10 в степени__']
        self.header_res = ['Мгновенное воспламенение, 1/год', 'Отложенное воспламенение, 1/год',
                           'Отложенное сгорание, 1/год', 'Ликвидация, 1/год']
        # используем формат общего GUI из calc_gui (package)
        self.min_gui = class_calc_gui.Minimal_GUI(columns=self.header)
        # для температуры вспышки изменим
        self.min_gui.form_elem[0].setRange(-100, 300)
        self.min_gui.form_elem[0].setSingleStep(1)
        # для степени изменим
        self.min_gui.form_elem[-1].setRange(-10, 0)
        self.min_gui.form_elem[-1].setSingleStep(1)
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.min_gui)
        # дадим кнопке функционал
        self.min_gui.btn_calc.clicked.connect(self.btn_calc_func)
        if not parent:
            self.show()

    def btn_calc_func(self) -> None:
        # получим все данные с полей формы
        val = self.min_gui.get_form_val()
        print(val)
        for i in val:  # проверка на 0
            if i == 0 and i != val[1]:
                return
        add_pow = math.pow(val[2], val[3])
        print(add_pow)
        # по кнопкам выбора определим пишем в excel/строим график
        if self.min_gui.write_excel.isChecked():
            # вычислим пожар пролива
            result = et.Event_tree().event_tree_inflammable(flash_temperature=val[0],
                                                            flow_rate=val[1], probability=add_pow)
            # запишем  в excel
            # проверим заполнялась ли шапка таблицы в экселе
            if self.table_header == 0:  # нет
                self.table_header = 1
                self.min_gui.Excel.create(self.header + self.header_res)

            val = val + result
            self.min_gui.Excel.write(val)
            print("усе")


        else:

            et.Event_tree().event_tree_inflammable(flash_temperature=val[0],
                                                   flow_rate=val[1], probability=add_pow)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.min_gui.closeEvent(event)


def log_uncaught_exceptions(ex_cls, ex, tb):
    # pyqt визуализация ошибок
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))
    print(text)
    QtWidgets.QMessageBox.critical(None, 'Error', text)
    sys.exit()


sys.excepthook = log_uncaught_exceptions
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Calc_GUI()
    app.exec_()
