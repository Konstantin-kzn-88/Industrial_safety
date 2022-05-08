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

    def explosion_point(self, mass: float, heat_of_combustion: float, z: float, radius: float) -> list:

        """
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param z: коэф. участия во взрыве (например z = 0.1)
        :param radius: расстояние от геометрического центра взрыва, м (например radius = 20)

        :return: : list: delta_p: избыточное давление ВУВ, кПа
                         impulse: импульс, Па*с
        """
        M_pr = (heat_of_combustion / 4520) * mass * z
        # поиск максимального значения давления и импульса
        for r in range(1, 2000):
            delta_p_max = 101.3 * ((0.8 * (M_pr ** 0.33) / r) + (3 * (M_pr ** 0.66)) /
                                   (r ** 2) + (5 * M_pr) / (r ** 3))
            impulse_max = 123 * (M_pr ** 0.66) / r
            if delta_p_max < 200:
                break

        delta_p = 101.3 * ((0.8 * (M_pr ** 0.33) / radius) + (3 * (M_pr ** 0.66)) /
                           (radius ** 2) + (5 * M_pr) / (radius ** 3))
        impulse = 123 * (M_pr ** 0.66) / radius
        if delta_p > 150:
            delta_p = delta_p_max
            impulse = impulse_max
        delta_p = round(delta_p, 2)
        impulse = round(impulse, 2)

        res = [delta_p, impulse]

        return res

    def explosion_array(self, mass: float, heat_of_combustion: float, z: float) -> list:

        """
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param z: коэф. участия во взрыве (например z = 0.1)

        :return: : list: [radius, delta_p_arr, impulse_arr, probit, probability]: список списков параметров
        """

        radius_arr = []
        delta_p_arr = []
        impulse_arr = []
        probit_arr = []
        probability_arr = []

        # максимальная интенсивность теплового излучения
        radius = 0.1
        delta_p = self.explosion_point(mass, heat_of_combustion, z, radius)[0]

        # просчитаем значения пока взрыв больше 2.9 кПА
        while delta_p > 2.9:
            res = self.explosion_point(mass, heat_of_combustion, z, radius)
            delta_p = res[0]
            impulse = res[1]
            probit = Probit().probit_explosion(delta_p, impulse)
            probability = Probit().probability(probit)
            # append
            radius_arr.append(round(radius, 2))
            delta_p_arr.append(delta_p)
            impulse_arr.append(impulse)
            probit_arr.append(probit)
            probability_arr.append(probability)
            radius += 0.1

        result = [radius_arr, delta_p_arr, impulse_arr, probit_arr, probability_arr]

        return result

    def explosion_plot(self, mass: float, heat_of_combustion: float, z: float) -> None:

        """
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param z: коэф. участия во взрыве (например z = 0.1)

         :return: None (matplotlib plot)
        """
        title = "Взрыв"
        x_lbl = "Расстояние, м"
        y_lbl_1 = "Изб.давление, кПа"
        y_lbl_2 = "Импульс, Па*с"
        y_lbl_3 = "Пробит-функция, -"
        y_lbl_4 = "Вероятность поражения, -"

        res_list = self.explosion_array(mass, heat_of_combustion, z)

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

    def explosion_class_zone(self, mass: float, heat_of_combustion: float, z: float) -> list:
        """
        :param mass: масса испарившегося вещества, кг
        :param heat_of_combustion: теплота сгорания, кДж/кг (например heat_of_combustion = 46000)
        :param z: коэф. участия во взрыве (например z = 0.1)

        :return: : list: [radius_CZA]: список отсортированных зон
        """

        res_list = self.explosion_array(mass, heat_of_combustion, z)

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
    mass = 2000
    heat_of_combustion = 46000
    z = 0.1
    radius = 500

    print(ev_class.explosion_class_zone(mass, heat_of_combustion, z))

    # ev_class = Explosion()
    #     # mass = 600*530*0.8
    #     # heat_of_combustion = 46000
    #     # z = 0.1
    #     # radius = 500
    #     #
    #     # print(ev_class.explosion_point(mass, heat_of_combustion, z, radius))
#     По ГОСТ delta_p=16.2, impulse=1000
