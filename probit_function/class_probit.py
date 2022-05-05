# -----------------------------------------------------------
# Класс предназначен для расчета пробит функции и
# определения вероятности поражения человека
# при воздействии поражающих факторов
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import math


class Probit:

    def probit_check(self, probit: float) -> float:
        """Проверка пробит функции:
        значения определены в интервале
        от 2.67 до 8.09"""
        if probit < 2.67:
            probit = 0
        elif probit > 8.09:
            probit = 8.09
        else:
            probit = probit
        return probit

    def probability(self, probit: float) -> float:
        """
        Вычисление вероятности поражения
        :param probit: значение пробит-функции

        :return: float
        """
        q_vp = -0.00064545 * (probit ** 6) + 0.02327 * (probit ** 5) - \
               0.33495 * (probit ** 4) + 2.4406 * (probit ** 3) - \
               9.41 * (probit ** 2) + 18.31 * (probit ** 1) - 14.156
        # проверка (вероятность гибели не может быть больше 1 и меньше 0
        if q_vp > 0.99:
            probability_death = 0.99
        elif q_vp < 0:
            probability_death = 0
        else:
            probability_death = q_vp

        return probability_death

    def probit_explosion(self, delta_P: float, impuls: float) -> float:
        """
        Вычисление пробит-функции при взрыве
        :param delta_P: избыточное давление, кПа
        :param impuls: давление насышенного пара, кПа

        :return: float
        """
        delta_P = delta_P * 1000  # кПа -> Па
        V1 = ((17500 / (delta_P)) ** (8.4)) + ((290 / impuls) ** (9.3))
        probit = 5 - 0.26 * math.log(V1)
        probit = self.probit_check(probit)

        return probit

    def probit_fireball(self, time: float, q_ball: float) -> float:
        """
        Вычисление пробит-функции при взрыве
        :param time: время существования, с
        :param q_ball: интенсивность теплового излучения, кВт/м2

        :return: float
        """
        probit = -12.8 + 2.56 * math.log(time * (q_ball ** (4 / 3)))
        probit = self.probit_check(probit)

        return probit

    def probit_strait_fire(self, dist: float, q_max: float) -> float:
        """
        Вычисление пробит-функции при взрыве
        :param dist: расстояние до зоны выхода
        :param q_max: максимальная интенсивность на заданном расстоянии, кВт/м2

        :return: float
        """
        t0 = 120  # время обнаружения пожара по методике, с
        speed = 1  # средняя скорость, м/с
        time = t0 + (dist*5 / speed)
        probit = -12.8 + 2.56 * math.log(time * (q_max ** (4 / 3)))
        probit = self.probit_check(probit)

        return probit


if __name__ == '__main__':
    ev_class = Probit()
    dist = 50
    q_max = 17
    print(ev_class.probit_strait_fire(dist, q_max))
    print(ev_class.probability(3.06))

    # ГОСТ 12.3.047-98 прил."Э"
    # ev_class = Probit()
    # delta_P=16.2
    # impuls= 1000
    # print(ev_class.probit_explosion(delta_P,impuls)) # 4.83
    # print(ev_class.probability(4.83)) #0.441 (В ГОСТ 0.43)

    # # ГОСТ 12.3.047-98 прил."Э"
    # ev_class = Probit()
    # time=40
    # q_ball= 12.9
    # print(ev_class.probit_fireball(time,q_ball)) # 3.28
    # print(ev_class.probability(3.28)) #0.004
    # разница значений из-за первого числа (в других НТД приведено
    # значение -12.8), поэтому оставил общепринятую практику
    # Pr = -14.9 + 2.56 * math.log(t * (q_ball ** (4 / 3)))

