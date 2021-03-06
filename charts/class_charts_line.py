# -----------------------------------------------------------
# Класс предназначен для построения кривых типа у=f(x)
# 1. у=f(x)
# 2. у1=f(x) у2=f(x) на одном графике при едином х
#
# (C) 2021 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------

import matplotlib.pyplot as plt


class Charts_line:

    def single_chart(self, title: str, x_lbl: str, y_lbl: str,
                     x_arr: list, y_arr: list, chart_lbl: str):
        """
        :param title: "Зависимость интенсивности теплового излучения от расстояния"
        :param x_lbl: "Расстояние, м"
        :param y_lbl: "Интенсивность, кВт/м2"
        :param x_arr: список расстояний, м
        :param y_arr: список воздействия, кВт/м2 (размерность в зависимости от функции)
        :param chart_lbl: "Интенсивность теплового излучения" (наименование построенной линии)
        :return: plt.show()
        """
        plt.title(title)
        plt.xlabel(x_lbl)
        plt.ylabel(y_lbl)
        plt.grid()
        plt.plot(x_arr, y_arr, label=chart_lbl)
        plt.legend()
        plt.show()

    def double_chart(self, title: str, x_lbl: str, y_lbl_1: str,
                     y_lbl_2: str, x_arr: list, y_arr_1: list,
                     y_arr_2: list, chart_lbl_1: str, chart_lbl_2: str):
        """

        :param title: "Зависимости: Pr(r), Qvp(r)"
        :param x_lbl: "Расстояние, м" (наименование х-оси)
        :param y_lbl_1: "Пробит-функция,-" (наименование у-оси)
        :param y_lbl_2: "Вероятность поражения, -" (наименование у-оси)
        :param x_arr: список расстояний, м
        :param y_arr_1: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_2: список воздействия, - (размерность в зависимости от функции)
        :param chart_lbl_1: "Pr" (наименование построенной линии)
        :param chart_lbl_2: "Qvp" (наименование построенной линии)
        :return: plt.show()
        """
        plt.figure(figsize=(9, 9))
        plt.subplot(2, 1, 1)
        plt.plot(x_arr, y_arr_1, label=chart_lbl_1, color='r')
        plt.title(title)
        plt.ylabel(y_lbl_1, fontsize=14)
        plt.grid(True)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(x_arr, y_arr_2, label=chart_lbl_2, color='k')
        plt.xlabel(x_lbl, fontsize=14)
        plt.ylabel(y_lbl_2, fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

    def triple_chart(self, title: str, x_lbl: str, y_lbl_1: str,
                     y_lbl_2: str, y_lbl_3: str, x_arr: list, y_arr_1: list,
                     y_arr_2: list, y_arr_3: list, chart_lbl_1: str,
                     chart_lbl_2: str, chart_lbl_3: str):
        """

        :param title: "Зависимости интенсивности излучения"
        :param x_lbl: "Расстояние, м" (наименование х-оси)
        :param y_lbl_1: "Интенсивность, кВт/м2" (наименование у-оси)
        :param y_lbl_2: "Пробит-функция, -" (наименование у-оси)
        :param y_lbl_3: "Вероятность поражения, -" (наименование у-оси)
        :param x_arr: список расстояний, м
        :param y_arr_1: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_2: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_3: список воздействия, - (размерность в зависимости от функции)
        :param chart_lbl_1: "Интенсивность" (наименование построенной линии)
        :param chart_lbl_2: "Pr" (наименование построенной линии)
        :param chart_lbl_2: "Qvp" (наименование построенной линии)
        :return: plt.show()
        """
        plt.figure(figsize=(9, 9))
        plt.subplot(3, 1, 1)
        plt.plot(x_arr, y_arr_1, label=chart_lbl_1, color='r')
        plt.title(title)
        plt.ylabel(y_lbl_1, fontsize=14)
        plt.grid(True)
        plt.legend()

        plt.subplot(3, 1, 2)
        plt.plot(x_arr, y_arr_2, label=chart_lbl_2, color='k')
        plt.ylabel(y_lbl_2, fontsize=14)
        plt.grid(True)
        plt.legend()

        plt.subplot(3, 1, 3)
        plt.plot(x_arr, y_arr_3, label=chart_lbl_3, color='b')
        plt.xlabel(x_lbl, fontsize=14)
        plt.ylabel(y_lbl_3, fontsize=14)
        plt.grid(True)
        plt.legend()

        #
        plt.show()

    def quadruple_chart(self, title: str, x_lbl: str, y_lbl_1: str,
                        y_lbl_2: str, y_lbl_3: str, y_lbl_4: str, x_arr: list, y_arr_1: list,
                        y_arr_2: list, y_arr_3: list, y_arr_4: list, chart_lbl_1: str,
                        chart_lbl_2: str, chart_lbl_3: str, chart_lbl_4: str):
        """

        :param title: "Зависимости интенсивности излучения"
        :param x_lbl: "Расстояние, м" (наименование х-оси)
        :param y_lbl_1: "Интенсивность, кВт/м2" (наименование у-оси)
        :param y_lbl_2: "Доза, кДж/м2" (наименование у-оси)
        :param y_lbl_3: "Пробит-функция, -" (наименование у-оси)
        :param y_lbl_4: "Вероятность поражения, -" (наименование у-оси)
        :param x_arr: список расстояний, м
        :param y_arr_1: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_2: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_3: список воздействия, - (размерность в зависимости от функции)
        :param y_arr_4: список воздействия, - (размерность в зависимости от функции)
        :param chart_lbl_1: "Интенсивность" (наименование построенной линии)
        :param chart_lbl_2: "Доза" (наименование построенной линии)
        :param chart_lbl_3: "Pr" (наименование построенной линии)
        :param chart_lbl_4: "Qvp" (наименование построенной линии)
        :return: plt.show()
        """
        plt.figure(figsize=(9, 9))
        plt.subplot(4, 1, 1)
        plt.plot(x_arr, y_arr_1, label=chart_lbl_1, color='r')
        plt.title(title)
        plt.ylabel(y_lbl_1, fontsize=12)
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.plot(x_arr, y_arr_2, label=chart_lbl_2, color='b')
        plt.ylabel(y_lbl_2, fontsize=12)
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 1, 3)
        plt.plot(x_arr, y_arr_3, label=chart_lbl_3, color='g')
        plt.ylabel(y_lbl_3, fontsize=12)
        plt.grid(True)
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(x_arr, y_arr_4, label=chart_lbl_4, color='k')
        plt.xlabel(x_lbl, fontsize=12)
        plt.ylabel(y_lbl_4, fontsize=12)
        plt.grid(True)
        plt.legend()
        #
        plt.show()


if __name__ == '__main__':
    pass
