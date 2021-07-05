import matplotlib.pyplot as plt

def triple_chart(title: str, x_lbl: str, y_lbl_1: str,
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
    plt.xlabel(x_lbl, fontsize=14)
    plt.ylabel(y_lbl_2, fontsize=14)
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(x_arr, y_arr_3, label=chart_lbl_3, color='r')
    plt.xlabel(x_lbl, fontsize=14)
    plt.ylabel(y_lbl_3, fontsize=14)
    plt.grid(True)
    plt.legend()


    #
    plt.show()


if __name__ == '__main__':
    triple_chart(title ="Intes", x_lbl="Dist", y_lbl_1="intesive",
    y_lbl_2="Pr", y_lbl_3="Q", x_arr=[5,4,3,2,1], y_arr_1=[5,4,3,2,1],
    y_arr_2=[1,2,3,4,5], y_arr_3=[5,4,3,2,1], chart_lbl_1="Int",
    chart_lbl_2="Prob", chart_lbl_3="Qvp")

