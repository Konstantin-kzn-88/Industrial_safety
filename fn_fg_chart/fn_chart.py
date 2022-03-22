import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def fn_chart(data: list):
    people = data[1]  # люди
    probability = data[0]  # вероятности
    unq = list(set(people))  # уникальные значение из people (люди)
    sum_ver = []  # сумма вероятностей для >= каждого уникального занчения

    for item_unq in unq:
        count = 0  # счетчик индекса для выбора индекса соответствующего probability
        res = 0  # результат сложения
        for iter in people:  # если значение из списка people
            if iter >= item_unq:  # больше чем item_unq из уникальных значений
                res += probability[count]  # проссумировать вероятности
            count += 1
        sum_ver.append(res)

    # Координаты для сплошных линий
    y = []
    for i in sum_ver:
        y.extend([i, i, None])
    y = y[:-4]

    x = []
    for i in range(len(unq) - 1):
        x.extend([unq[i], unq[i + 1], None])
    x.extend([unq[-1], unq[-1], None])
    x = x[:-4]

    # Координаты для пунктирных линий
    y1 = []
    for i in range(len(sum_ver) - 1):
        y1.extend([sum_ver[i], sum_ver[i + 1], None])
    y1 = y1[:-4]

    x1 = []
    for i in range(len(unq) - 1):
        x1.extend([unq[i + 1], unq[i + 1], None])
    x1 = x1[:-4]

    # Построение графика
    fig, ax = plt.subplots()

    ax.plot(x, y, 'bo', linewidth=2, linestyle='-')
    #  Устанавливаем интервал основных делений:
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    ax.plot(x1, y1, color='b', linewidth=2, linestyle='--')
    ax.set_yscale("log")

    #  Прежде чем рисовать вспомогательные линии
    #  необходимо включить второстепенные деления
    #  осей:
    ax.minorticks_on()

    #  Определяем внешний вид линий основной сетки:
    ax.grid(which='major',
            color='k',
            linewidth=0.5)

    #  Определяем внешний вид линий вспомогательной
    #  сетки:
    ax.grid(which='minor',
            color='k',
            linestyle=':')

    ax.set_title('F/N - диаграмма')
    ax.set_xlabel('Количество погибших, чел')
    ax.set_ylabel('Вероятность, 1/год')

    fig.set_figwidth(12)
    fig.set_figheight(8)

    plt.show()


if __name__ == '__main__':
    data = [
        [3e-2, 3e-2, 3e-3, 3e-5, 3e-5],
        [0, 1, 2, 3, 4]
    ]
    y = fn_chart(data)
