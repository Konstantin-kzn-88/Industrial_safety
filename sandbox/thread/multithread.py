import threading
from shapely.geometry import Point
from shapely.geometry import LineString
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
import numpy as np
import time

start_time = time.time()

def calc_el_zeors_array_for_point(width, height, coord, probit):
    # сделаем нулевую матрицу по размерам картинки
    zeors_array = np.zeros((width, height))
    # для каждой точки картинки определим силу воздействия заданных точек
    for x in range(width):
        for y in range(height):
            # определим расстояние от перебираемой точки картинки до
            # заданной точки coord
            dist = round(Point(x, y).distance(Point(coord[0], coord[1])))
            # крайний случай, когда перебираемая точка и заданная точка coord равны
            # тогда воздействие максимально
            if dist == 0:
                zeors_array[x, y] = zeors_array[x, y] + probit[0][0]

            # если расстояние есть в дистанции силы воздействия
            elif dist in probit[1]:
                # найдем индекс
                find_index = probit[1].index(dist)
                # запишем силу воздействия в матрицу (т.е. если в этой точке воздействие от другой точки уже
                # было, то воздействия суммируются)
                zeors_array[x, y] = zeors_array[x, y] + probit[0][find_index]


    return zeors_array

# создадим функцию которая по суммарному воздейсатвию определяет цвет пикселя
def color_px(x, y):
    if res_arr[x, y] >= 0.9:
        px[x, y] = red
    elif 0.9 > res_arr[x, y] >= 0.7:
        px[x, y] = yellow
    elif 0.7 > res_arr[x, y] >= 0.5:
        px[x, y] = light_blue
    elif 0.5 > res_arr[x, y] >= 0.3:
        px[x, y] = green
    elif 0.3 > res_arr[x, y] >= 0.2:
        px[x, y] = blue
    elif 0.2 > res_arr[x, y] >= 0.1:
        px[x, y] = purple


def wrapme(calc_el_zeors_array_for_point, res, width, height, coord_all, probit_all):
    res.append(calc_el_zeors_array_for_point(width, height, coord_all, probit_all))


# Решение
start_time = time.time()
# цвета для отображения результата
red = (255, 0, 0, 70)
yellow = (255, 255, 0, 70)
light_blue = (0, 255, 255, 70)
green = (0, 255, 0, 70)
blue = (0, 0, 255, 70)
purple = (255, 0, 255, 70)

# возьмем чистую картинку
im = Image.open('image.jpg')
# измерим размер
width, height = im.size
# загрузим в память
px = im.load()

# Сделаем несколько точек и покажем их воздействие
# точки с координатами
point_1 = [150, 150]
point_2 = [90, 90]
point_3 = [250, 330]
point_4 = [400, 300]
point_5 = [100, 250]
point_6 = [400, 100]
point_7 = [250, 400]
# сила воздействия от 0,99 до 0
power = [i / 100 for i in range(100)]
power.sort(reverse=True)  # сила нужна по убыванию, чем дальше от точки воздействия тем меньше сила
probit_point_1 = [power, [i for i in range(100)]]  # [[сила воздействия],[на расстоянии от точки]]
probit_point_2 = [power, [i for i in range(100)]]
probit_point_3 = [power, [i for i in range(100)]]
probit_point_4 = [power, [i for i in range(100)]]
probit_point_5 = [power, [i for i in range(100)]]
probit_point_6 = [power, [i for i in range(100)]]
probit_point_7 = [power, [i for i in range(100)]]
# список всех точек (их координат) и список их влияния (силы воздействия)
coord_all = [point_1, point_2, point_3, point_4, point_5, point_6, point_7]
probit_all = [probit_point_1, probit_point_2, probit_point_3, probit_point_4,
              probit_point_5, probit_point_6, probit_point_7]

res = []

for i in range(0, len(coord_all)):
    name = f't{i}'
    name = threading.Thread(target=wrapme, args=(calc_el_zeors_array_for_point, res, width, height, coord_all[i], probit_all[i],))
    name.start()
    name.join()

res_arr = np.zeros((width, height))
for k in res:
    res_arr = res_arr + res

print(len(res_arr[0,0]))
# представим суммарное воздействие от точек
# for x in range(width):
#     for y in range(height):
#         print(res_arr[x,y])
#         # color_px(x, y)

# выведем результат как картинку
im.show(title="result")
print("--- %s секунд ---" % (time.time() - start_time))

# ПРИМЕР МАССИВА 3 на 3
# import threading
# import numpy as np
#
#
# # Посчитаем уравнение y=x **2 + 4*x
#
# def func_1(width, height):
#     zeors_array = np.zeros((width, height))
#     zeors_array[0, 0] = 1
#     return zeors_array
#
#
# def func_2(width, height):
#     zeors_array = np.zeros((width, height))
#     zeors_array[1, 1] = 1
#     return zeors_array
#
#
# def wrapme(func, res, *args, **kwargs):
#     res.append(func(*args, **kwargs))
#
#
# # допустим x = 2
# width, height = 3, 3
# res = []
#
# t1 = threading.Thread(target=wrapme, args=(func_1, res, width, height,))
# t2 = threading.Thread(target=wrapme, args=(func_2, res, width, height,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
#
# print(res[0]+res[1])

#Пример со stackoverflow

# import threading
#
# # Посчитаем уравнение y=x **2 + 4*x
#
# def square_number(x):
#     y1 = x ** 2
#     return y1
#
#
# def quadruple_num(x):
#     y2 = 4 * x
#     return y2
#
#
# def wrapme(func, res, *args, **kwargs):
#     res.append(func(*args, **kwargs))
#
#
# # допустим x = 2
# x = 2
# res = []
#
# t1 = threading.Thread(target=wrapme, args=(square_number, res, x,))
# t2 = threading.Thread(target=wrapme, args=(quadruple_num, res, x,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
#
# print(sum(res))  # 12