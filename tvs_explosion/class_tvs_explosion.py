# -----------------------------------------------------------
# Класс предназначен для расчета взрыва ТВС
#
# CП 12.13130-2009
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

from charts import Charts_line
from probit_function import Probit


class Explosion:

    def burn_rate(self, class_substance: int, view_space: int, mass: float) -> float:  # скорость горения
        """
        :param class_substance: класс взрывоопасности вещества (1-4)
        :param view_space: класс окружающего пространства (1-4)
        :param mass: масса испарившегося вещества, кг
        :return: : float: v_burn_rate
        """

        if class_substance == 1:
            if view_space == 1:
                v_burn_rate = 500
            elif view_space == 2:
                v_burn_rate = 500
            elif view_space == 3:
                v_burn_rate = 300
            elif view_space == 4:
                v_burn_rate = 200
            else:
                v_burn_rate = 200

        elif class_substance == 2:
            if view_space == 1:
                v_burn_rate = 500
            elif view_space == 2:
                v_burn_rate = 300
            elif view_space == 3:
                v_burn_rate = 200
            elif view_space == 4:
                v_burn_rate = 150
            else:
                v_burn_rate = 150

        elif class_substance == 3:
            if view_space == 1:
                v_burn_rate = 300
            elif view_space == 2:
                v_burn_rate = 200
            elif view_space == 3:
                v_burn_rate = 150
            elif view_space == 4:
                v_burn_rate = 43 * (mass) ** (1 / 6)
            else:
                v_burn_rate = 43 * (mass) ** (1 / 6)

        elif class_substance == 4:
            if view_space == 1:
                v_burn_rate = 200
            elif view_space == 2:
                v_burn_rate = 150
            elif view_space == 3:
                v_burn_rate = 43 * (mass) ** (1 / 6)
            elif view_space == 4:
                v_burn_rate = 26 * (mass) ** (1 / 6)
            else:
                v_burn_rate = 26 * (mass) ** (1 / 6)

        else:
            if view_space == 1:
                v_burn_rate = 200
            elif view_space == 2:
                v_burn_rate = 150
            elif view_space == 3:
                v_burn_rate = 43 * (mass) ** (1 / 6)
            elif view_space == 4:
                v_burn_rate = 26 * (mass) ** (1 / 6)
            else:
                v_burn_rate = 26 * (mass) ** (1 / 6)

        return v_burn_rate

    def explosion_point(self, class_substance: int, view_space: int, mass: float,
                        heat_of_combustion: float, sigma: int, energy_level: int, radius: int) -> list:

        """
        :param class_substance: класс взрывоопасности вещества (1-4)
        :param view_space: класс окружающего пространства (1-4)
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param sigma: тип смеси  (4- парогазовая, 7 - газовая)
        :param energy_level: тип ТВС  (1- легкая, 2 - тяжелая)
        :param radius: расстояние от геометрического центра взрыва, м (например radius = 20)

        :return: : list: delta_p: избыточное давление ВУВ, кПа
                         impulse: импульс, Па*с
        """
        v_burn_rate = self.burn_rate(class_substance, view_space, mass)

        E = mass * heat_of_combustion * energy_level * 1000

        if E < 1:
            E = 0.1 * heat_of_combustion * energy_level * 1000

        Rx = radius / ((E / 101300) ** (1 / 3))
        if Rx > 0.34:
            Rx = radius / ((E / 101300) ** (1 / 3))
        elif Rx <= 0.34:
            Rx = 0.34

        delta_p = ((v_burn_rate / 340) ** 2) * \
                  (((sigma - 1) / sigma) * ((0.83 / Rx) - 0.14 / (Rx ** 2))) * 101.3

        impulse = (v_burn_rate / 340) * ((sigma - 1) / sigma) * \
                  (1 - 0.4 * (v_burn_rate / 340) * ((sigma - 1) / sigma)) * \
                  (0.06 / Rx + 0.01 / (Rx ** 2) - 0.0025 / (Rx ** 3)) * \
                  (101325 ** (2 / 3)) * (E ** (1 / 3)) / 340

        delta_p = round(delta_p, 2)
        impulse = round(impulse, 2)

        res = [delta_p, impulse]

        return res

    def explosion_array(self, class_substance: int, view_space: int, mass: float,
                        heat_of_combustion: float, sigma: int, energy_level: int) -> list:

        """
        :param class_substance: класс взрывоопасности вещества (1-4)
        :param view_space: класс окружающего пространства (1-4)
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param sigma: тип смеси  (4- парогазовая, 7 - газовая)
        :param energy_level: тип ТВС  (1- легкая, 2 - тяжелая)

        :return: : list: [radius, delta_p_arr, impulse_arr, probit, probability]: список списков параметров
        """

        radius_arr = []
        delta_p_arr = []
        impulse_arr = []
        probit_arr = []
        probability_arr = []

        # максимальная интенсивность теплового излучения
        radius = 1
        delta_p = self.explosion_point(class_substance, view_space,
                                       mass, heat_of_combustion, sigma,
                                       energy_level, radius)[0]

        # просчитаем значения пока взрыв больше 2.9 кПА
        while delta_p > 2.9:
            res = self.explosion_point(class_substance, view_space,
                                       mass, heat_of_combustion, sigma,
                                       energy_level, radius)
            delta_p = res[0]
            impulse = res[1]
            probit = Probit().probit_explosion(delta_p, impulse)
            probability = Probit().probability(probit)
            # append
            radius_arr.append(radius)
            delta_p_arr.append(delta_p)
            impulse_arr.append(impulse)
            probit_arr.append(probit)
            probability_arr.append(probability)
            radius += 0.5

        result = [radius_arr, delta_p_arr, impulse_arr, probit_arr, probability_arr]

        return result

    def explosion_plot(self, class_substance: int, view_space: int, mass: float,
                       heat_of_combustion: float, sigma: int, energy_level: int) -> None:

        """
        :param class_substance: класс взрывоопасности вещества (1-4)
        :param view_space: класс окружающего пространства (1-4)
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param sigma: тип смеси  (4- парогазовая, 7 - газовая)
        :param energy_level: тип ТВС  (1- легкая, 2 - тяжелая)

         :return: None (matplotlib plot)
        """
        title = "Взрыв"
        x_lbl = "Расстояние, м"
        y_lbl_1 = "Изб.давление, кПа"
        y_lbl_2 = "Импульс, Па*с"
        y_lbl_3 = "Пробит-функция, -"
        y_lbl_4 = "Вероятность поражения, -"

        res_list = self.explosion_array(class_substance, view_space,
                                        mass, heat_of_combustion, sigma,
                                        energy_level)

        x_arr = res_list[0]
        y_arr_1 = res_list[1]
        y_arr_2 = res_list[2]
        y_arr_3 = res_list[3]
        y_arr_4 = res_list[4]

        chart_lbl_1 = "dP"
        chart_lbl_2 = "i"
        chart_lbl_3 = "Pr"
        chart_lbl_4 = "P"

        Charts_line.quadruple_chart(self, title, x_lbl, y_lbl_1, y_lbl_2,
                                    y_lbl_3, y_lbl_4, x_arr, y_arr_1, y_arr_2, y_arr_3, y_arr_4,
                                    chart_lbl_1, chart_lbl_2, chart_lbl_3, chart_lbl_4)

    def explosion_class_zone(self, class_substance: int, view_space: int, mass: float,
                             heat_of_combustion: float, sigma: int, energy_level: int) -> list:
        """
        :param class_substance: класс взрывоопасности вещества (1-4)
        :param view_space: класс окружающего пространства (1-4)
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param sigma: тип смеси  (4- парогазовая, 7 - газовая)
        :param energy_level: тип ТВС  (1- легкая, 2 - тяжелая)

        :return: : list: [radius_CZA]: список отсортированных зон
        """

        res_list = self.explosion_array(class_substance, view_space,
                                        mass, heat_of_combustion, sigma,
                                        energy_level)

        # Calculate classified_zone_array
        classified_zone_array = [100, 53, 28, 12, 5, 3]  # CZA
        radius_CZA = []
        delta_p_array = res_list[1]
        radius_array = res_list[0]

        for CZA in classified_zone_array:
            sort = list(filter((lambda x: CZA + 5 > x > CZA - 0.1), delta_p_array))
            if sort == []:
                radius_CZA.append(0)
            else:
                sort = min(sort)
                radius_CZA.append(round(radius_array[delta_p_array.index(sort)], 2))
        return radius_CZA


if __name__ == '__main__':
    ev_class = Explosion()
    class_substance = 4
    view_space = 4
    mass = 2000
    heat_of_combustion = 4600
    sigma = 7
    energy_level = 2

    ev_class.explosion_plot(class_substance, view_space,
                            mass, heat_of_combustion, sigma,
                            energy_level)

    # ev_class = Explosion()
    # class_substance = 4
    # view_space = 2
    # mass = 2000
    # heat_of_combustion = 4600
    # sigma = 7
    # energy_level = 2
    #
    # ev_class.explosion_plot(class_substance, view_space,
    #                         mass, heat_of_combustion, sigma,
    #                         energy_level)
