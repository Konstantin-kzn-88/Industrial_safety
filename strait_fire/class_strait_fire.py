# -----------------------------------------------------------
# Класс предназначен для расчета пожара пролива
# на открытой местности
#
# Приказ МЧС № 404 от 10.07.2009
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math
from charts import Charts_line
from probit_function import Probit


class Strait_fire:

    def termal_radiation_point(self, S_spill: float, m_sg: float, mol_mass: float,
                               t_boiling: float, wind_velocity: float, radius: float) -> float:

        """
        :param S_spill: площадь пролива, м2
        :param m_sg: удельная плотность выгорания, кг/(с*м2) (например m_sg = 0.06)
        :param mol_mass: молекулярная масса, кг/кмоль (например mol_mass = 95.3)
        :param t_boiling: температура кипения, град.С (например t_boiling = 68)
        :param wind_velocity: скорость ветра, м/с (например wind_velocity = 2)
        :param radius: расстояние от геометрического центра пролива, м (например radius = 20)

        :return: : float: q_term: интенсивность теплового излучения, кВт/м2
        """
        # Вычислим эффективный диаметр
        D_eff = math.sqrt(4 * S_spill / math.pi)
        # проведем проверку не попадает ли расчетная точка в пролив
        if radius < (D_eff / 2 + 0.1):  # попадает
            # примем радиус на границе пролива, так как методика
            # не работает внутри пролива, т.е. делается допущение
            # что внутри пролива интенсивность та же что и на границе
            radius = (D_eff / 2 + 0.1)

        po_steam = mol_mass / (22.413 * (1 + 0.00367 * t_boiling))
        u_star = wind_velocity / math.pow((m_sg * 9.8 * D_eff) / po_steam, (1 / 3))

        if u_star >= 1:  # L
            flame_length = 55 * D_eff * math.pow(m_sg / (1.15 * math.sqrt(9.81 * D_eff)), 0.67) * math.pow(u_star,
                                                                                                           0.21)  # L
        else:
            flame_length = 42 * D_eff * math.pow(m_sg / (1.15 * math.sqrt(9.81 * D_eff)), 0.61)

        cos_tetta = 1 if u_star < 1 else math.pow(u_star, (-0.5))

        tetta = math.acos(cos_tetta)  # in radians
        a_pr = 2 * flame_length / D_eff
        b_pr = 2 * radius / D_eff
        A_pr = math.sqrt(a_pr * a_pr + math.pow(b_pr + 1, 2) - 2 * a_pr * (b_pr + 1) * math.sin(tetta))
        B_pr = math.sqrt(a_pr * a_pr + math.pow(b_pr - 1, 2) - 2 * a_pr * (b_pr - 1) * math.sin(tetta))
        C_pr = math.sqrt(1 + (math.pow(b_pr, 2) - 1) * math.pow(math.cos(tetta), 2))
        D_pr = math.sqrt((b_pr - 1) / (b_pr + 1))
        E_pr = (a_pr * math.cos(tetta)) / (b_pr - a_pr * math.sin(tetta))
        F_pr = math.sqrt(math.pow(b_pr, 2) - 1)

        Fv = (1 / math.pi) * (-E_pr * math.atan(D_pr) +
                              E_pr * ((math.pow(a_pr, 2) + math.pow(b_pr + 1, 2) - 2 * b_pr * (
                        1 + a_pr * math.sin(tetta))) / (A_pr * B_pr)) *
                              math.atan((A_pr * D_pr) / B_pr) + (math.cos(tetta) / C_pr) *
                              (math.atan((a_pr * b_pr - F_pr * F_pr * math.sin(tetta)) / (F_pr * C_pr)) +
                               math.atan(F_pr * F_pr * math.sin(tetta) / (F_pr * C_pr))))

        Fh = (1 / math.pi) * (
                math.atan(1 / D_pr) + (math.sin(tetta) / C_pr) *
                (math.atan((a_pr * b_pr - F_pr * F_pr * math.sin(tetta)) / (F_pr * C_pr)) +
                 math.atan((math.pow(F_pr, 2) * math.sin(tetta)) / (F_pr * C_pr))) -
                ((math.pow(a_pr, 2) + math.pow(b_pr + 1, 2) - 2 * (b_pr + 1 + a_pr * b_pr * math.sin(tetta))) / (
                        A_pr * B_pr)) *
                math.atan(A_pr * D_pr / B_pr)
        )

        Fq = math.sqrt(math.pow(Fv, 2) + math.pow(Fh, 2))

        tay = math.exp(-7 * math.pow(10, -4) * (radius - 0.5 * D_eff))

        E_f = 140 * math.pow(2.7, -0.12 * D_eff) + 20 * (1 - math.pow(2.7, -0.12 * D_eff))

        q_term = Fq * tay * E_f

        return q_term

    def termal_radiation_array(self, S_spill: float, m_sg: float, mol_mass: float,
                               t_boiling: float, wind_velocity: float) -> list:

        """
        :param S_spill: площадь пролива, м2
        :param m_sg: удельная плотность выгорания, кг/(с*м2) (например m_sg = 0.06)
        :param mol_mass: молекулярная масса, кг/кмоль (например mol_mass = 95.3)
        :param t_boiling: температура кипения, град.С (например t_boiling = 68)
        :param wind_velocity: скорость ветра, м/с (например wind_velocity = 2)

        :return: : list: [radius, q_term, probit, probability]: список списков параметров
        """

        radius_arr = []
        q_term_arr = []
        probit_arr = []
        probability_arr = []

        # максимальная интенсивность теплового излучения
        radius = 1
        q_term = self.termal_radiation_point(S_spill, m_sg, mol_mass, t_boiling, wind_velocity, radius)

        # просчитаем значения пока интенсивность теплового излучения больше 1.2 кВт/м2
        while q_term > 1.2:
            q_term = round(self.termal_radiation_point(S_spill, m_sg, mol_mass,
                                                       t_boiling, wind_velocity, radius), 2)
            q_term_arr.append(q_term)
            radius_arr.append(radius)
            radius += 1
        # расчитаем пробит функцию и вероятность поражения
        D_eff = (4 * S_spill / 3.14) ** (1 / 2)
        # Определим расстояние на котором интенсивность = 4 кВт/м2
        r_4_kw = 0
        for q in q_term_arr:
            if q < 4:
                r_4_kw = radius_arr[q_term_arr.index(q)]
                break

        for i in radius_arr:
            dist = r_4_kw - i  # расстояние до точки на которой интенсивность = 4 кВт/м2

            if i < D_eff:
                probit = 8.09
                probability = 0.99
            elif dist < 0:
                probit = 0
                probability = 0
            else:
                probit = Probit().probit_strait_fire(dist, q_term_arr[radius_arr.index(i)])
                probability = Probit().probability(probit)
            probit_arr.append(probit)
            probability_arr.append(probability)

        result = [radius_arr, q_term_arr, probit_arr, probability_arr]

        return result

    def strait_fire_plot(self, S_spill: float, m_sg: float, mol_mass: float,
                         t_boiling: float, wind_velocity: float) -> None:

        """
        :param S_spill: площадь пролива, м2
        :param m_sg: удельная плотность выгорания, кг/(с*м2) (например m_sg = 0.06)
        :param mol_mass: молекулярная масса, кг/кмоль (например mol_mass = 95.3)
        :param t_boiling: температура кипения, град.С (например t_boiling = 68)
        :param wind_velocity: скорость ветра, м/с (например wind_velocity = 2)

         :return: None (matplotlib plot)
        """
        title = "Интенсивность излучения"
        x_lbl = "Расстояние, м"
        y_lbl_1 = "Интенсивность, кВт/м2"
        y_lbl_2 = "Пробит-функция, -"
        y_lbl_3 = "Вероятность поражения, -"

        res_list = self.termal_radiation_array(S_spill, m_sg, mol_mass,
                                               t_boiling, wind_velocity)

        x_arr = res_list[0]
        y_arr_1 = res_list[1]
        y_arr_2 = res_list[2]
        y_arr_3 = res_list[3]

        chart_lbl_1 = "q"
        chart_lbl_2 = "Pr"
        chart_lbl_3 = "P"

        Charts_line.triple_chart(self, title, x_lbl, y_lbl_1, y_lbl_2,
                                 y_lbl_3, x_arr, y_arr_1, y_arr_2, y_arr_3,
                                 chart_lbl_1, chart_lbl_2, chart_lbl_3)

    def termal_class_zone(self, S_spill: float, m_sg: float, mol_mass: float,
                          t_boiling: float, wind_velocity: float):
        """
        :param S_spill: площадь пролива, м2
        :param m_sg: удельная плотность выгорания, кг/(с*м2) (например m_sg = 0.06)
        :param mol_mass: молекулярная масса, кг/кмоль (например mol_mass = 95.3)
        :param t_boiling: температура кипения, град.С (например t_boiling = 68)
        :param wind_velocity: скорость ветра, м/с (например wind_velocity = 2)

        :return: : list: [radius_CZA]: список отсортированных зон
        """

        res_list = self.termal_radiation_array(S_spill, m_sg, mol_mass,
                                               t_boiling, wind_velocity)

        # Calculate classified_zone_array
        classified_zone_array = [10.5, 7.0, 4.2, 1.4]  # CZA
        radius_CZA = []
        q_term_array = res_list[1]
        radius_array = res_list[0]

        for CZA in classified_zone_array:
            sort = list(filter((lambda x: CZA + 0.3 > x > CZA - 0.1), q_term_array))
            if sort == []:
                radius_CZA.append(0)
            else:
                sort = min(sort)
                radius_CZA.append(round(radius_array[q_term_array.index(sort)], 2))

        return radius_CZA


if __name__ == '__main__':
    ev_class = Strait_fire()
    S_spill = 10
    m_sg = 0.06
    mol_mass = 95
    t_boiling = 68
    wind_velocity = 2

    print(ev_class.termal_class_zone(S_spill, m_sg, mol_mass,
                                     t_boiling, wind_velocity))

    # ev_class = Strait_fire()
    # S_spill= 918
    # E_f= 47
    # m_sg=0.06
    # mol_mass=95
    # t_boiling=68
    # wind_velocity=2
    # radius=40
    #
    # print(ev_class.termal_radiation_point(S_spill,E_f,m_sg,mol_mass,
    #                                       t_boiling,wind_velocity,radius))

    # ev_class = Strait_fire()
    # S_spill = 20
    # m_sg = 0.06
    # mol_mass = 95
    # t_boiling = 68
    # wind_velocity = 2
    #
    # title = "Plot"
    # x_lbl = "Dist,m"
    # y_lbl_1 = "heat"
    # y_lbl_2 = "Pr"
    # y_lbl_3 = "Q"
    #
    # res_list = ev_class.termal_radiation_array(S_spill, m_sg, mol_mass,
    #                                            t_boiling, wind_velocity)
    #
    # x_arr = res_list[0]
    # y_arr_1 = res_list[1]
    # y_arr_2 = res_list[2]
    # y_arr_3 = res_list[3]
    #
    # chart_lbl_1 = "heat"
    # chart_lbl_2 = "Pr"
    # chart_lbl_3 = "Q"
    #
    # ev_class.strait_fire_plot(title, x_lbl, y_lbl_1, y_lbl_2,
    #                           y_lbl_3, x_arr, y_arr_1, y_arr_2, y_arr_3,
    #                           chart_lbl_1, chart_lbl_2, chart_lbl_3)

    #
