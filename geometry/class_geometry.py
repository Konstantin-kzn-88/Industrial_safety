import math


# Зависимости для сравнения
# from shapely.geometry import Point
# from shapely.geometry import LineString


class Pos_point:
    """
    Вспомогательный класс для функции intersection_segmets
    класса Geometry
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Geometry:

    def distance_point_to_point(self, object_: list, point_: list) -> float:
        """
        Вычисление расстояния между 2 точками

        Пример:
        distance_point_to_point(object_=[1, 1], point_=[3, 3])

        :return: distance - расстояние между 2 точками
        """
        x = point_[0]
        y = point_[1]
        x1 = object_[0]
        y1 = object_[1]

        distance = round(math.sqrt(pow(x1 - x, 2) + pow(y1 - y, 2)))
        return distance

    def distance_point_to_segment(self, object_, point_) -> float:
        """
        Функция расстояния от точки до отрезка

        Пример:
        distance_point_to_segment(object_=[1, 1, 20, 10], point_=[10, 50])

        :return: distance - расстояние между точкой и отрезком
        """
        cx = point_[0]
        cy = point_[1]
        ax = object_[0]
        ay = object_[1]
        bx = object_[2]
        by = object_[3]

        # избегать ошибки деления на ноль
        a = max(by - ay, 0.00001)
        b = max(ax - bx, 0.00001)
        # вычислить перпендикулярное расстояние до прямой
        dl = abs(a * cx + b * cy - b * ay - a * ax) / math.sqrt(a ** 2 + b ** 2)
        # вычислить точку пересечения
        x = ((a / b) * ax + ay + (b / a) * cx - cy) / ((b / a) + (a / b))
        y = -1 * (a / b) * (x - ax) + ay
        # определить, попадает ли точка пересечения на отрезок прямой
        if (ax <= x <= bx or bx <= x <= ax) and (ay <= y <= by or by <= y <= ay):
            distance = dl
            return int(distance)
        else:
            # если это не так, то вернуть минимальное расстояние до конечной точки отрезка
            distance = min(math.sqrt((ax - cx) ** 2 + (ay - cy) ** 2), math.sqrt((bx - cx) ** 2 + (by - cy) ** 2))
            return round(distance, 2)

    def distanse_point_to_line(self, object_: list, point_: list) -> float:
        """
        Функция определения расстояния минимального от точки до линии состоящей
        из отрезков (линия непрерывна).

        Пример:
        distanse_point_to_line(object_=[1, 1, 20, 10, 40, 30], point_=[10, 50]

        :return: distance - расстояние между точкой и линией
        """

        all_distance = []
        for i in range(0, len(object_) - 2, 2):
            segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
            distance = self.distance_point_to_segment(segment, point_)
            all_distance.append(distance)

        return round(min(all_distance), 2)

    def point_in_polygon(self, object_: list, point_: list) -> bool:
        """
        Функция определения входит ли точка в произвольный
        не пересекающийся многоугольник методом "трассировки лучами". Если луч из
        искомой точки пересекает нечетное количество граней,
        то точка принадлежит многоугольнику.
        https://grafika.me/node/70

        Пример вызова:
        point_in_polygon(object_=[3, 3, 6, 3, 6, 6, 4, 9, 3, 6], point_=[1, 9]

        :return: True/ False (входит / не входит)
        """
        # 1. Замкнем грани фигуры
        object_ = object_ + object_[:2]
        # 2. Принадлежит ли точка граням многоугольника
        if self.distanse_point_to_line(object_, point_) == 0:
            return True
        # 3. Определим область трассировки.
        # минимальные и максимальные х и у для трассоровки.
        x_max = max(object_[::2]) * 2
        y_max = max(object_[1::2]) * 2

        # 3. Создадим лучи и проверим сколько граней они пересекают
        # от точки (0,0) с шагом 45 градусов на 360 градусов, 8 лучей.
        x_ray = [0, point_[0], x_max, x_max, x_max, point_[0], 0, 0]
        y_ray = [0, 0, 0, point_[1], y_max, y_max, y_max, point_[1]]

        # 4. Определим для каждого луча, пересекает ли он грани
        result = []
        for i in range(0, len(x_ray)):
            for j in range(0, len(object_) - 2, 2):  # перебор граней
                segment = [object_[j], object_[j + 1], object_[j + 2], object_[j + 3]]
                result.append(self.intersection_segmets(point_, segment, [x_ray[i], y_ray[i]]))

        # 5. Определим количество граней фигуры
        face = (len(object_) - 2) // 2

        # 6. Определим сколько граней каждый луч пересекал
        for k in range(0, len(result), face):
            list_ = result[k:k + face:1]
            # Если количество граней не четно, то точка принадлежит многоугольнику
            if list_.count(True) % 2 != 0:
                return True

        return False

    def intersection_segmets(self, point_: list, segment: list, point_end: list) -> bool:
        """
        Функция определения пересечения отрезков (point_, point_end) и (segment).
        Пример вызова:
        intersection_segmets(point_=[1, 1], segment=[6, 3, 6, 6], point_end=[8, 4])
        Решение взято:
        (https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/)
        :return: True/ False (Пересекаются / не пересекаются)
        """

        a = Pos_point(point_[0], point_[1])
        b = Pos_point(point_end[0], point_end[1])
        c = Pos_point(segment[0], segment[1])
        d = Pos_point(segment[2], segment[3])

        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

        return intersect(a, b, c, d)

    def square_polygon(self, object_: list) -> int:
        """
        Функция вычисления площади произвольного многоугольника по
        координатам вершин.
        https://ru.wikipedia.org/wiki/%D0%A4%D0%BE%D1%80%D0%BC%D1%83%D0%BB%D0%B0_%D0%BF%D0%BB%D0%BE%D1%89%D0%B0%D0%B4%D0%B8_%D0%93%D0%B0%D1%83%D1%81%D1%81%D0%B0

        Пример:
        square_polygon([5,1,5,1,8,8,13,-10,-34,10])

        :return: square (площадь в условных единицах)
        """
        sum_for_x = object_[0::2]
        sum_for_y = object_[3::2] + object_[1:2]
        sub_for_x = object_[2::2] + object_[0:1]
        sub_for_y = object_[1::2]

        sum_ = sum([x * y for x, y in zip(sum_for_x, sum_for_y)])
        sub_ = sum([x * y for x, y in zip(sub_for_x, sub_for_y)]) * (-1)
        square = int((1 / 2) * abs((sum_ + sub_)))

        return square

    def length_line(self,object_:list) -> float:
        """
        Функция вычисления длины произвольной линии
        состоящей из отрезков.

        Пример:
        length_line([5,1,5,1,8,8,13,-10,-34,10])

        :return: length сумму длин всех отрезков
        """

        all_length_line = []
        for i in range(0, len(object_) - 2, 2):
            distance = self.distance_point_to_point([object_[i], object_[i + 1]], [object_[i + 2], object_[i + 3]])
            all_length_line.append(distance)
        length = round(sum(all_length_line), 2)
        return length


if __name__ == "__main__":
    ...

    # # 1. Расстояние от точки до точки
    # # 1.1. Расчет
    # calc = Geometry().distance_point_to_point(object_=[1, 1], point_=[3, 3])
    # print(f'Расстояние до точки расчет. {calc}')
    # # 1.2. Shapely
    # point_1 = Point(1, 1)
    # point_2 = Point(3, 3)
    # print(f'Расстояние до точки shapely. {round(point_1.distance(point_2))}')
    # print('*'*20)
    #
    # # 2. Расстояние от точки до отрезка
    # # 2.1. Расчет
    # calc = Geometry().distance_point_to_segment(object_=[1, 1, 20, 10], point_=[10, 50])
    # print(f'Расстояние до отрезка расчет. {calc}')
    # # 2.2. Shapely
    # point_3 = Point(10, 50)
    # segment = LineString([(1, 1), (20, 10)])
    # dist = round(point_3.distance(segment))
    # print(f'Расстояние до отрезка shapely {dist}')
    # print('*' * 20)
    #
    # # 3. Расстояние от точки до ломанной линии состоящей из непрерывных отрезков
    # # 3.1. Расчет
    # calc = Geometry().distanse_point_to_line(object_=[1, 1, 20, 10, 40, 30], point_=[10, 50])
    # print(f'Расстояние до линии расчет. {calc}')
    # # 3.2. Shapely
    # point_4 = Point(10, 50)
    # line = LineString([(1, 1), (20, 10), (40, 30)])
    # dist_2 = round(point_4.distance(line))
    # print(f'Расстояние до линии shapely {dist_2}')
    # print('*' * 20)
    #
    # calc = Geometry().point_in_polygon(object_=[3, 3, 6, 3, 6, 6, 4, 9, 3, 6], point_=[1, 9])
    # print(f'Точка лежит в многоугольнике? Ответ: {calc}')
    #
    # calc = Geometry().intersection_segmets(point_=[1, 1], segment=[6, 3, 6, 6], point_end=[8, 4])
    # print(f'Пересекаются отрезки (point_, point_end) и (segment)? Ответ: {calc}')
    # print('*' * 20)

    # calc = Geometry().square_polygon([5,1,5,1,8,8,13,-10,-34,10])
    # print(f'Площадь многоугольника в усл.ед.: {calc}')

    # print('*' * 20)

    calc = Geometry().length_line([5,1,5,1,8,8,13,-10,-34,10])
    print(f'Длина ломанной линии.: {calc}')
