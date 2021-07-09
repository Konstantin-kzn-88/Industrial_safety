# -----------------------------------------------------------
# Класс предназначен для расчета "огненного шара"
#
# Приказ МЧС № 404 от 10.07.2009
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math
from charts import Charts_line
from probit_function import Probit


class Fireball:

    def fireball_point(self, mass: float, ef: float, radius: float) -> list:

        """
        :param mass: масса огненного шара, кг
        :param ef: ср.поверхностная плотность теплового излучения, кВт/м2 (например ef = 450)
        :param radius: расстояние от геометрического центра пролива, м (например radius = 20)

        :return: : list: q_term: интенсивность теплового излучения, кВт/м2
                         d_term: доза теплового излучения, кДж/м2
        """
        D_eff = 5.33 * (mass ** 0.327)
        H_eff = D_eff / 2
        t_s = 0.92 * (mass ** 0.303)

        Fq = (H_eff / D_eff + 0.5) / (4 * ((((H_eff / D_eff + 0.5) ** 2) + ((radius / D_eff) ** 2)) ** 1.5))

        tay = math.exp(-7 * (10 ** (-4) * (((radius ** 2 + H_eff ** 2) ** (1 / 2)) - D_eff / 2)))

        q_ball = round(ef * Fq * tay, 2)
        d_term = round(q_ball * t_s, 2)

        res = [q_ball, d_term]

        return res

    def fireball_array(self, mass: float, ef: float) -> list:

        """
        :param mass: масса огненного шара, кг
        :param ef: ср.поверхностная плотность теплового излучения, кВт/м2 (например ef = 450)

        :return: : list: [radius, q_term, d_term, probit, probability]: список списков параметров
        """

        radius_arr = []
        q_term_arr = []
        d_term_arr = []
        probit_arr = []
        probability_arr = []

        # максимальная интенсивность теплового излучения
        radius = 1
        q_term = self.fireball_point(mass, ef, radius)[0]
        t_s = 0.92 * (mass ** 0.303)

        # просчитаем значения пока интенсивность теплового излучения больше 1.2 кВт/м2
        while q_term > 1.2:
            res = self.fireball_point(mass, ef, radius)
            q_term = res[0]
            d_term = res[1]
            probit = Probit().probit_fireball(t_s, q_term)
            probability = Probit().probability(probit)
            # append
            radius_arr.append(radius)
            q_term_arr.append(q_term)
            d_term_arr.append(d_term)
            probit_arr.append(probit)
            probability_arr.append(probability)
            radius += 0.5

        result = [radius_arr, q_term_arr, d_term_arr, probit_arr, probability_arr]

        return result

    def fireball_plot(self, mass: float, ef: float) -> None:

        """
        :param mass: масса огненного шара, кг
        :param ef: ср.поверхностная плотность теплового излучения, кВт/м2 (например ef = 450)

         :return: None (matplotlib plot)
        """
        title = "Огненный шар"
        x_lbl = "Расстояние, м"
        y_lbl_1 = "Интенсивность, кВт/м2"
        y_lbl_2 = "Доза, кДж/м2"
        y_lbl_3 = "Пробит-функция, -"
        y_lbl_4 = "Вероятность поражения, -"

        res_list = self.fireball_array(mass, ef)

        x_arr = res_list[0]
        y_arr_1 = res_list[1]
        y_arr_2 = res_list[2]
        y_arr_3 = res_list[3]
        y_arr_4 = res_list[4]

        chart_lbl_1 = "q"
        chart_lbl_2 = "Q"
        chart_lbl_3 = "Pr"
        chart_lbl_4 = "P"

        Charts_line.quadruple_chart(self, title, x_lbl, y_lbl_1, y_lbl_2,
                                    y_lbl_3, y_lbl_4, x_arr, y_arr_1, y_arr_2, y_arr_3, y_arr_4,
                                    chart_lbl_1, chart_lbl_2, chart_lbl_3, chart_lbl_4)

    def termal_class_zone(self, mass: float, ef: float) -> list:
        """
        :param mass: масса огненного шара, кг
        :param ef: ср.поверхностная плотность теплового излучения, кВт/м2 (например ef = 450)

        :return: : list: [radius_CZA]: список отсортированных зон
        """

        res_list = self.fireball_array(mass, ef)

        # Calculate classified_zone_array
        classified_zone_array = [600, 320, 220, 120]  # CZA
        radius_CZA = []
        d_term_array = res_list[2]
        radius_array = res_list[0]

        for CZA in classified_zone_array:
            sort = list(filter((lambda x: CZA + 10 > x > CZA - 0.1), d_term_array))
            if sort == []:
                radius_CZA.append(0)
            else:
                sort = min(sort)
                radius_CZA.append(round(radius_array[d_term_array.index(sort)], 2))
        return radius_CZA


if __name__ == '__main__':
    ev_class = Fireball()
    mass = 2.54 * (10 ** 5)
    ef = 450

    print(ev_class.termal_class_zone(mass, ef))

    # ГОСТ 12.3.047-98 прил.Д
    # ev_class = Fireball()
    # mass = 2.54 * (10 ** 5)
    # ef = 450
    # radius = 500
    #
    # print(ev_class.fireball_point(mass, ef, radius)) (по ГОСТ q_ball=12.9)
