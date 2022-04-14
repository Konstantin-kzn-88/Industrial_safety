import math


from shapely.geometry import Point
from shapely.geometry import LineString


class Distance:
    def __init__(self):
        ...

    def distance_point_to_point(self, object_, point_):
        """
        Вычисление расстояния между 2 точками
        :return: distance - расстояние между 2 точками
        """
        x = point_[0]
        y = point_[1]
        x1 = object_[0]
        y1 = object_[1]

        distance = round(
            math.sqrt(pow(x1 - x, 2) + pow(y1 - y, 2)))
        return distance

    def distance_point_to_segment(self, object_, point_):
        """
        Функция расстояния от точки до отрезка
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
            return int(distance)

    def distanse_point_to_line(self, object_, point_):

        all_distance = []

        for i in range(0, len(object_) - 2, 2):
            segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
            distance =self.distance_point_to_segment(segment, point_)
            all_distance.append(distance)

        return int(min(all_distance))


if __name__ == "__main__":
    calc = Distance().distance_point_to_point(object_=[2, 2], point_=[10, 50])
    print(calc)

    calc = Distance().distance_point_to_segment(object_=[1, 1, 20, 10], point_=[10, 50])
    print(calc)

    calc = Distance().distanse_point_to_line(object_=[1, 1, 20, 10, 40, 30], point_=[10, 50])
    print(calc)

# #     тест c shapely
point_1 = [10, 50]
coord_line = LineString([(1, 1), (20, 10), (40,30)])
dist = round(Point(point_1[0], point_1[1]).distance(coord_line))
print(dist)
