# -----------------------------------------------------------
# Графический интерфейс предназначен для расчета пожара пролива
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from PySide2 import QtWidgets, QtCore, QtGui
from pathlib import Path
import traceback

# local import
from strait_fire import class_strait_fire as sf
from calc_gui import class_calc_gui


class Calc_GUI(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        QtWidgets.QWidget.__init__(self, parent)
        self.table_header = 0  # установлена ли шабка для талицы
        # Иконка и название
        self.setWindowTitle('Расчет пожара пролива (Приказ МЧС 404)')
        self.setWindowIcon(QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/calc_ico.png'))
        # списки для таблицы (шапка)
        self.table_header = 0  # установлена ли шабка для талицы
        self.header = ['Площадь пролива, м2', 'Уд.масс. скорость, кг(с*м2)', 'Мол.масса, кг/кмоль',
                       'Тем-ра кипения, гр.С', 'Скорость вертра, м/c']
        self.header_res = ['Интенсивность (10.5) кВт/м2', 'Интенсивность (7.0) кВт/м2',
                           'Интенсивность (4.2) кВт/м2', 'Интенсивность (1.4) кВт/м2']
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
        for i in val: # проверка на 0
            if i == 0:
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText("Введено нулевое значение!")
                msg.exec()
                return
        # по кнопкам выбора определим пишем в excel/строим график
        if self.min_gui.write_excel.isChecked():
            # вычислим пожар пролива
            result = sf.Strait_fire().termal_class_zone(S_spill=val[0], m_sg=val[1], mol_mass=val[2],
                                                      t_boiling=val[3], wind_velocity=val[4])
            # запишем  в excel
            # проверим заполнялась ли шапка таблицы в экселе
            if self.table_header == 0:  # нет
                self.table_header = 1
                self.min_gui.Excel.create(self.header + self.header_res)

            val = val + result
            self.min_gui.Excel.write(val)


        else:

            sf.Strait_fire().strait_fire_plot(S_spill=val[0], m_sg=val[1], mol_mass=val[2],
                                              t_boiling=val[3], wind_velocity=val[4])

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
