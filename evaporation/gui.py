# -----------------------------------------------------------
# Графический интерфейс предназначен для расчета испарения веществ
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
import win32com.client
from pathlib import Path


#local import
from evaporation import class_evaporation_liguid
from mini_gui import class_minimal_gui

col2 = ['Мол.масса, кг/кмоль', 'Давление пара, кПа', 'Площадь пролива, м2',
       'Масса ж.ф., кг', 'Время испарения, c']

class Calc_GUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.min_gui = class_minimal_gui.Minimal_GUI(columns=col2)
        layout = QtWidgets.QFormLayout(self)
        layout.addRow(self.min_gui)
        # дадим кнопке функционал
        self.min_gui.btn_calc.clicked.connect(self.btn_calc_func)
        if not parent:
            self.show()

    def btn_calc_func(self):
        print("Ура мы в новом модуле!!!!")

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.min_gui.closeEvent(event)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Calc_GUI()
    app.exec_()



# class Calc_GUI(QWidget):
#    def __init__(self):
#        super().__init__()
#        self.initUI()
#        # запустим эксель
#        self.Excel = win32com.client.Dispatch("Excel.Application")
#        self.wb = self.Excel.Workbooks.Add()
#        self.Excel.Visible = 1
#        self.sheet = self.wb.ActiveSheet
#        #создадим заголовки таблицы (row,col)
#        self.sheet.Cells(1, 1).value = 'Мол.масса, кг/кмоль'
#        self.sheet.Cells(2, 1).value = 'Pн, кПа'
#        self.sheet.Cells(3, 1).value = 'S, м2'
#        self.sheet.Cells(4, 1).value = 'Мж, кг'
#        self.sheet.Cells(5, 1).value = 't, c'
#        self.sheet.Cells(6, 1).value = 'Мисп, кг'
#        self.sheet.Range("A1").ColumnWidth = 20
#
#
#    def initUI(self):
#        # Заголовок и иконка для GUI
#        self.setWindowTitle('Расчет испарения вещества (СП 12.13130-2009)')
#        self.setWindowIcon(QIcon(str(Path(os.getcwd()).parents[0]) +'/ico/calc_ico.png'))
#        #  Создаем валидаторы для полей ввода
#        onlyInt = QIntValidator()  # only int
#        onlyDouble = QDoubleValidator()  # only float
#
#        # создаем сетку из двух колонок
#        # окно для текста help
#        # окно для ввода данных
#        grid = QGridLayout(self)
#        grid.setColumnStretch(0, 1)
#        grid.setColumnStretch(1, 1)
#
#
#        # создаем окошки для ввода данных
#        self.molecular_weight = QLineEdit()               #Мол.масса, кмоль/кг
#        self.molecular_weight.setValidator(onlyDouble)
#        self.molecular_weight.setPlaceholderText("Мол.масса, кмоль/кг")
#
#
#        self.vapor_pressure = QLineEdit()               # Давление пара, кПа
#        self.vapor_pressure.setValidator(onlyDouble)
#        self.vapor_pressure.setPlaceholderText("Давление пара, кПа")
#
#        self.spill_area = QLineEdit()               # Площадь пролива, м2
#        self.spill_area.setValidator(onlyDouble)
#        self.spill_area.setPlaceholderText("Площадь пролива, м2")
#
#        self.max_mass = QLineEdit()               # Макс.масса вещества, кг
#        self.max_mass.setValidator(onlyDouble)
#        self.max_mass.setPlaceholderText("Макс.масса вещества, кг")
#
#        self.time = QLineEdit()               # Время испарения, с
#        self.time.setValidator(onlyDouble)
#        self.time.setPlaceholderText("Время испарения, с")
#
#        #  создаем радио кнопки для выбора действия
#        self.write_excel = QRadioButton('Записать в Excel')
#        self.write_excel.setChecked(True)
#        self.plot_graph = QRadioButton('Построить график испарения')
#        # создаем кнопку расчета которая на основе радио кнопок
#        # произведет нужный расчет или построит график
#        self.btn_calc = QPushButton("Расчет")
#        self.btn_calc.clicked.connect(self.btn_calc_func)
#        # основно текст help окна
#        self.help_txt = QTextEdit("<b>СП 12.13130-2009 </b><br>"
#                                  "<b>Основные исходные данные:</b><br>"
#                                  "- Мол.масса, кмоль/кг<br>"
#                                  "- Давление пара, кПа<br>"
#                                  "- Площадь пролива, м2 <br>"
#                                  "- Макс.масса вещества, кг <br>"
#                                  "- Время испарения, с <br>"
#                                  "<b>Основные выходные данные:</b><br>"
#                                  "- Расчет испарения в Excel<br>"
#                                  "- График испарения вещества<br>")
#        self.help_txt.setReadOnly(True)
#
#
#        # упаковываем в контейнер и в сетку
#        vbox = QVBoxLayout(self)
#        vbox.setContentsMargins(0, 0, 0, 0)
#        box = QGroupBox(self)
#        vbox.addWidget(self.molecular_weight)
#        vbox.addWidget(self.vapor_pressure)
#        vbox.addWidget(self.spill_area)
#        vbox.addWidget(self.max_mass)
#        vbox.addWidget(self.time)
#        vbox.addWidget(self.write_excel)
#        vbox.addWidget(self.plot_graph)
#        vbox.addWidget(self.btn_calc)
#        box.setLayout(vbox)
#
#        vbox_help = QVBoxLayout(self)
#        vbox_help.setContentsMargins(0, 0, 0, 0)
#        box_help = QGroupBox(self)
#        vbox_help.addWidget(self.help_txt)
#        box_help.setLayout(vbox_help)
#
#
#        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
#
#        grid.addWidget(box_help, 0, 0, -1, 1)
#        grid.addWidget(box, 0, 1, 1, 1)
#        grid.addItem(verticalSpacer, 1, 1, 1, 1)
#
#        self.setLayout(grid)
#
#        self.move(300, 200)
#        self.show()
#
#
#
#    def btn_calc_func(self):
#        # Получить значения из полей
#        molecular_weight = str(self.molecular_weight.displayText())
#        vapor_pressure = str(self.vapor_pressure.displayText())
#        spill_area = str(self.spill_area.displayText())
#        max_mass = str(self.max_mass.displayText())
#        time = str(self.time.displayText())
#        # замена разделителей если вдруг запятая
#        molecular_weight = molecular_weight.replace(",", ".")
#        vapor_pressure = vapor_pressure.replace(",", ".")
#        spill_area = spill_area.replace(",", ".")
#        max_mass = max_mass.replace(",", ".")
#        time = time.replace(",", ".")
#
#        # Проверка заполнения полей, что бы не было пустым,
#        # пока поля не будут заполнены никакие расчеты произведены не будут
#        check_filling = [molecular_weight, vapor_pressure, spill_area, max_mass, time]
#        if "" in check_filling:
#            msg = QMessageBox(self)
#            msg.setIcon(QMessageBox.Warning)
#            msg.setWindowTitle("Информация")
#            msg.setText("Указананы не все исходные данные!")
#            msg.exec()
#            return
#
#        # превращаем переменные в числа после
#        # считывания с полей ввода
#        molecular_weight = float(molecular_weight)
#        vapor_pressure = float(vapor_pressure)
#        spill_area = float(spill_area)
#        max_mass = float(max_mass)
#        time = float(time)
#        # смотря какой check нажат рисуем график/заполняем excel
#        if self.write_excel.isChecked():
#            # запишем данные в эксель
#            sheet = self.wb.ActiveSheet
#            mass = class_evaporation_liguid.Evapor_liqud().evapor_liguid(molecular_weight, vapor_pressure, spill_area, max_mass, time)
#
#            res_list = []
#            res_list.append(molecular_weight)
#            res_list.append(vapor_pressure)
#            res_list.append(spill_area)
#            res_list.append(max_mass)
#            res_list.append(time)
#            res_list.append(mass)
#
#            # ищем пустой столбец для записи в файле экселя
#            i = 1
#            while i < 1000:
#                # т.е. строка постоянно 1, а столбец мы ищем перебором
#                val = sheet.Cells(1, i).value
#                if val == None:
#                    break
#                i = i + 1
#            # когда мы нашли пустой столбец
#            # нам в цикле нужно его заполнить
#            # данными из списка radius_CZA
#            k = 1
#            for rec in res_list:
#                sheet.Cells(k, i).value = rec
#                k = k + 1
#
#        elif self.plot_graph.isChecked():
#            # нужно построить график на основании данных которые
#            # есть в полях
#            class_evaporation_liguid.Evapor_liqud().evapor_plot(molecular_weight,vapor_pressure,spill_area,max_mass)
#
#
#    def closeEvent(self, e):
#        """
#        Функция закрытия окна с дополнительным диалогом
#        на закрытие файла (да/нет)
#        """
#        result = QMessageBox.question(self, "Подтверждение закрытия окна",
#                                      "Вы действительно хотите закрыть окно? Excel не будет сохранен.",
#                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
#        if result == QMessageBox.Yes:
#             self.wb.Close(SaveChanges=False)
#                # Закроем COM объект
#             self.Excel.Quit()
#             e.accept()
#             QWidget.closeEvent(self, e)
#        else:
#             e.ignore()
#
# def my_excepthook(type, value, tback):
#    #  функция отлова ошибок на PyQt5
#    QMessageBox.critical(
#        window, "CRITICAL ERROR", str(value),
#        QMessageBox.Cancel
#    )
#
#    sys.__excepthook__(type, value, tback)
#
#
# sys.excepthook = my_excepthook
#
#
#
#
# if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = Calc_GUI()
#    sys.exit(app.exec_())
