import math


def power_data_old(max_r, probit):
    """
    Функция которая в зависимости от максимального радиуса и вероятности
    дает распределение ероятности поражение
    """
    radius = []
    power = [i / 100 for i in range(100)]

    for i in power:
        radius.append(max_r * i)
    power.sort(reverse=True)
    power = [i * probit for i in power]
    power_data = [power, radius]

    return power_data


def power_data(max_r, probit):
    """
    Функция которая в зависимости от максимального радиуса и вероятности
    дает распределение ероятности поражение
    """

    def mod_tan(x):
        """
        Функция тангенсального распределения
        (больше всего подходит на настоящий пробит)
        """
        var = math.tan(x)
        if var > 1:
            result = 1
        else:
            result = var
        return result

    radius = []
    L = [i / 100 for i in range(100)]
    power = list(map(lambda x: mod_tan(x), L))

    for i in L:
        radius.append(round((max_r * i),2))
    power.sort(reverse=True)
    power = [i * probit for i in power]
    power_data = [power, radius]

    return power_data

if __name__ == '__main__':
    pwd = power_data_old(60, 1)
    print(pwd)
    print("-" * 200)
    pwd = power_data(60, 1)
    print(pwd)
    print("-" * 200)
