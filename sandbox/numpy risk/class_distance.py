import math

from shapely.geometry import Point
from shapely.geometry import LineString

class Pos_point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


class Distance:
    def __init__(self):
        ...

    def distance_point_to_point(self, object_, point_) -> int:
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

    def distance_point_to_segment(self, object_, point_) -> int:
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

    def distanse_point_to_line(self, object_, point_) -> int:

        all_distance = []

        for i in range(0, len(object_) - 2, 2):
            segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
            distance = self.distance_point_to_segment(segment, point_)
            all_distance.append(distance)

        return int(min(all_distance))

    def point_in_polygon(self, object_, point_) -> bool:
        object_ = object_ + object_[:2] # замкнуть полигон
        # 1. Принадлежит ли точка граням многоугольника
        if self.distanse_point_to_line(object_, point_) == 0:
            return True
        # Минимальные и максимальные х и у для области поиска
        x_max = max(object_[::2]) * 2
        y_max = max(object_[1::2]) * 2
        # 2. Создадим лучи и проверим сколько граней они пересекают
        x_ray = [i * (x_max / 10) for i in range(0, 11)]
        y_ray = [i * (y_max / 10) for i in range(0, 11)]
        print(x_ray, y_ray)


        # Проверим лучами по оси ХO
        for x in x_ray:
            res = []
            for i in range(0, len(object_) - 2, 2):
                segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
                res.append(self.intersection_segmets(point_, segment, [x, 0]))
                print(segment, [round(x,1), 0], self.intersection_segmets(point_, segment, [x, 0]))



        print("+"*50)
        # Проверим лучами по оси OY
        for y in y_ray:
            res = []
            for i in range(0, len(object_) - 2, 2):
                segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
                res.append(self.intersection_segmets(point_, segment, [0, y]))
                print(segment, [0, round(y,1)], self.intersection_segmets(point_, segment, [0, y]))



        print("+" * 50)
        # Проверим лучами по оси ХYmax
        for x in x_ray:
            res = []
            for i in range(0, len(object_) - 2, 2):
                segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
                res.append(self.intersection_segmets(point_, segment, [x, y_max]))
                print(segment, [round(x,1), y_max], self.intersection_segmets(point_, segment, [x, y_max]))


        print("+"*50)
        # Проверим лучами по оси OY
        for y in y_ray:
            res = []
            for i in range(0, len(object_) - 2, 2):
                segment = [object_[i], object_[i + 1], object_[i + 2], object_[i + 3]]
                res.append(self.intersection_segmets(point_, segment, [x_max, y]))
                print(segment, [x_max, round(y,1)], self.intersection_segmets(point_, segment, [x_max, y]))


    def intersection_segmets(self, point_, segment, point_end):
        a = Pos_point(point_[0], point_[1])
        b = Pos_point(point_end[0], point_end[1])
        c = Pos_point(segment[0], segment[1])
        d = Pos_point(segment[2], segment[3])

        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        def intersect(A, B, C, D):
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        return intersect(a,b,c,d)






if __name__ == "__main__":
    # calc = Distance().distance_point_to_point(object_=[1, 1], point_=[10, 50])
    # print(f'Расстояние до точки расчет. {calc}')
    #
    # calc = Distance().distance_point_to_segment(object_=[1, 1, 20, 10], point_=[10, 50])
    # print(f'Расстояние до отрезка расчет. {calc}')
    #
    # calc = Distance().distanse_point_to_line(object_=[1, 1, 20, 10, 40, 30], point_=[10, 50])
    # print(f'Расстояние до линии расчет. {calc}')

    calc = Distance().point_in_polygon(object_=[3, 3, 6, 3, 6, 6, 3, 6], point_=[1, 1])
    print(calc)
    #
    # calc = Distance().intersection_segmets(point_=[1, 1], segment=[6, 3, 6, 6], point_end=[8, 4])
    # print(calc)

    # #     тест c shapely
    # point_1 = [10, 50]
    # segment = LineString([(1, 1), (20, 10)])
    # dist = round(Point(point_1[0], point_1[1]).distance(segment))
    # print(f'Расстояние до отрезка shapely {dist}')
    # line = LineString([(5, 5), (20, 10), (40, 30)])
    # dist_2 = round(Point(point_1[0], point_1[1]).distance(line))
    # print(f'Расстояние до линии shapely {dist_2}')
