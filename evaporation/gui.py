# -----------------------------------------------------------
# Графический интерфейс предназначен для расчета испарения веществ
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
import traceback

# local import
from evaporation import class_evaporation_liguid as ev
from calc_gui import class_calc_gui

class Calc_GUI(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.table_header = 0  # установлена ли шабка для талицы
        # Иконка и название
        self.setWindowTitle('Расчет испарения вещества (СП 12.13130-2009)')
        self.setWindowIcon(QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/calc_ico.png'))
        # списки для таблицы (шапка)
        self.table_header = 0  # установлена ли шабка для талицы
        self.header = ['Мол.масса, кг/кмоль', 'Давление пара, кПа', 'Площадь пролива, м2',
               'Масса ж.ф., кг', 'Время испарения, c']
        self.header_res = ['Масса испарившегося в-ва, кг']
        # используем формат общего GUI из calc_gui (package)
        self.min_gui = class_calc_gui.Minimal_GUI(columns=self.header)
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
        # по кнопкам выбора определим пишем в excel/строим график
        if self.min_gui.write_excel.isChecked():
            # вычислим массу испарившегся вещества, кг
            mass = ev.Evapor_liqud().evapor_liguid(molecular_weight=val[0],
                                                   vapor_pressure=val[1],
                                                   spill_area=val[2],
                                                   max_mass=val[3], time=val[4])
            # запишем расчетную массу в excel
            # проверим заполнялась ли шапка таблицы в экселе
            if self.table_header == 0:  # нет
                self.table_header = 1
                self.min_gui.Excel.create(self.header+self.header_res)

            val.append(mass)
            self.min_gui.Excel.write(val)


        else:

            # нужно построить график на основании данных которые
            # есть в полях
            ev.Evapor_liqud().evapor_plot(molecular_weight=val[0],
                                          vapor_pressure=val[1],
                                          spill_area=val[2],
                                          max_mass=val[3])

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
