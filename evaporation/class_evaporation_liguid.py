# -----------------------------------------------------------
# Класс предназначен для расчета испарения жидкости
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
import math
from charts import Charts_line

max_time_evapor = 3600  # по НТД максимальное время испарения составляет 3600 с


class Evapor_liqud:

    def evapor_liguid(self, molecular_weight: float, vapor_pressure: float,
                      spill_area: float, max_mass: float, time: int):
        """
        :param molecular_weight: молекулярная масса, кг/кмоль
        :param vapor_pressure: давление насышенного пара, кПа
        :param spill_area: площадь пролива, м2
        :param max_mass: максимально возможная масса при испарении, кг
        :param time: максимальное время испарения, с

        :return: : int: mass: масса испарившейся жидкости, кг
        """
        mass = round((math.pow(molecular_weight, 1 / 2)) * math.pow(10, -6) * vapor_pressure * time * spill_area, 3)
        if mass > max_mass:
            mass = max_mass
        return mass

    def evapor_plot(self, molecular_weight: float, vapor_pressure: float,
                    spill_area: float, max_mass: float):
        """
        :param molecular_weight: молекулярная масса, кг/кмоль
        :param vapor_pressure: давление насышенного пара, кПа
        :param spill_area: площадь пролива, м2
        :param max_mass: максимально возможная масса при испарении, кг

        :return: None (matplotlib plot)
        """
        x_arr = []  # значения по оси х
        y_arr = []  # значения по оси у
        for time in range(1, max_time_evapor + 1):
            mass = self.evapor_liguid(molecular_weight, vapor_pressure, spill_area, max_mass, time)
            x_arr.append(time)
            y_arr.append(mass)
        title = "Зависимость исперания жидкости от времени"
        x_lbl = "Время, с"
        y_lbl = "Масса, кг"
        chart_lbl = "Испарение"
        Charts_line.single_chart(self, title, x_lbl, y_lbl, x_arr, y_arr, chart_lbl)



if __name__ == '__main__':
    ev_class = Evapor_liqud()
    molecular_weight = 147.3
    vapor_pressure = 0.87
    spill_area = 3
    max_mass = 3
    ev_class.evapor_plot(molecular_weight, vapor_pressure, spill_area, max_mass)

    # # пример №17 стр.25 Пособие по НПБ 105-95
    # ev_class = Evapor_liqud()
    # molecular_weight = 147.3
    # vapor_pressure = 0.87
    # spill_area = 3
    # max_mass = 3
    # time = 3600
    # mass = ev_class.evapor_liguid(molecular_weight, vapor_pressure, spill_area, max_mass, time)
    # print(f"Масса испарившегося вещества составляет {mass} кг.")
