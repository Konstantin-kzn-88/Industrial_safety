import math

from shapely.geometry import Point
# from shapely.geometry import LineString
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import time

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
point_1 = [150,150]
point_2 = [90,90]
point_3 = [250,330]
point_4 = [400,300]
point_5 = [100,250]
point_6 = [400,100]
point_7 = [250,400]
# сила воздействия от 0,99 до 0
power = [i/100 for i in range(100)]
power.sort(reverse=True) # сила нужна по убыванию, чем дальше от точки воздействия тем меньше сила
probit_point_1 = [power,[i for i in range(100)]] # [[сила воздействия],[на расстоянии от точки]]
probit_point_2 = [power,[i for i in range(100)]]
probit_point_3 = [power,[i for i in range(100)]]
probit_point_4 = [power,[i for i in range(100)]]
probit_point_5 = [power,[i for i in range(100)]]
probit_point_6 = [power,[i for i in range(100)]]
probit_point_7 = [power,[i for i in range(100)]]
# список всех точек (их координат) и список их влияния (силы воздействия)
coord_all = [point_1, point_2, point_3, point_4, point_5, point_6, point_7]
probit_all = [probit_point_1, probit_point_2, probit_point_3, probit_point_4,
              probit_point_5, probit_point_6, probit_point_7]

#
# # for line_obj
# probit_line = [[0.99,0.7,0.3,0.2,0.1],[1,2,3,4,5]]
# coord_line = LineString([(70, 70), (30, 70)])
#
# probit_line_2 = [[0.99,0.7,0.3,0.2,0.1],[1,2,3,4,5]]
# coord_line_2 = LineString([(90, 90), (30, 90)])
#
# probit_line_3 = [[0.99,0.7,0.3,0.2,0.1],[1,2,3,4,5]]
# coord_line_3 = LineString([(50, 100), (50, 0)])
#
# probit_line_4 = [[0.99,0.7,0.3,0.2,0.1],[1,2,3,4,5]]
# coord_line_4 = LineString([(0, 100), (100, 0)])
#
# probit_line_all = [probit_line,probit_line_2,probit_line_3,probit_line_4]
# coord_line_all = [coord_line,coord_line_2,coord_line_3,coord_line_4]



# сделаем нулевую матрицу по размерам картинки
zeors_array = np.zeros((width, height))

# создадим функцию которая по суммарному воздейсатвию определяет цвет пикселя
def color_px(x,y):
    if zeors_array[x, y] >= 0.9:
        px[x, y] = red
    elif 0.9 > zeors_array[x, y] >= 0.7:
        px[x, y] = yellow
    elif 0.7 > zeors_array[x, y] >= 0.5:
        px[x, y] = light_blue
    elif 0.5 > zeors_array[x, y] >= 0.3:
        px[x, y] = green
    elif 0.3 > zeors_array[x, y] >= 0.2:
        px[x, y] = blue
    elif 0.2 > zeors_array[x, y] >= 0.1:
        px[x, y] = purple

# создадим функцию которая принимает высоту, ширину картинки, список координат,
# координаты точек и силу их воздействия вокруг себя
def calc_el_zeors_array_for_point(width, height, coord, probit):
    # для каждой точки картинки определим силу воздействия заданных точек
    for x in range(width):
        for y in range(height):
            # определим расстояние от перебираемой точки картинки до
            # заданной точки coord
            dist = round(Point(x, y).distance(Point(coord[0], coord[1])))
            # dist = round(math.sqrt(pow(coord[0] - x, 2) + pow(coord[1] - y, 2)))
            # крайний случай, когда перебираемая точка и заданная точка coord равны
            # тогда воздействие максимально
            if dist == 0:
                zeors_array[x, y] = zeors_array[x, y] + probit[0][0]
                color_px(x,y)
            # если расстояние есть в дистанции силы воздействия
            elif dist in probit[1]:
                # найдем индекс
                find_index = probit[1].index(dist)
                # запишем силу воздействия в матрицу (т.е. если в этой точке воздействие от другой точки уже
                # было, то воздействия суммируются)
                zeors_array[x, y] = zeors_array[x, y] + probit[0][find_index]
                color_px(x, y)

# def calc_el_zeors_array_for_line(width, height, coord_line,probit_line):
#     for x in range(width):
#         for y in range(height):
#             dist = round(Point(x, y).distance(coord_line))
#             if dist == 0:
#                 zeors_array[x, y] = zeors_array[x, y] + probit_line[0][0]
#             if dist in probit_line[1]:
#                 find_index = probit_line[1].index(dist)
#                 zeors_array[x, y] = zeors_array[x, y] + probit_line[0][find_index]



# переберем все точки
for elem in coord_all:
    # определим индекс
    find_index = coord_all.index(elem)
    # вызовем функцию суммарного воздействия
    calc_el_zeors_array_for_point(width, height, coord_all[find_index], probit_all[find_index])

# for elem_line in coord_line_all:
#     find_index_line = coord_line_all.index(elem_line)
#     print(find_index_line)
#     print(probit_line_all[find_index_line])
#     print(coord_line_all[find_index_line])
#     calc_el_zeors_array_for_line(width, height, coord_line_all[find_index_line], probit_line)


# calc_el_zeors_array_for_line(width, height, coord_line_all, probit_line_all)



# # представим суммарное воздействие от точек
# for x in range(width):
#     for y in range(height):
#         if zeors_array[x,y] >= 0.9:
#             px[x, y] = red
#         elif 0.9 > zeors_array[x,y] >= 0.7:
#             px[x, y] = yellow
#         elif 0.7 > zeors_array[x,y] >= 0.5:
#             px[x, y] = light_blue
#         elif 0.5 > zeors_array[x,y] >= 0.3:
#             px[x, y] = green
#         elif 0.3 > zeors_array[x,y] >= 0.2:
#             px[x, y] = blue
#         elif 0.2 > zeors_array[x,y] >= 0.1:
#             px[x, y] = purple

# выведем результат как картинку
im.save('res.png')

print("--- %s секунд ---" % (time.time() - start_time))


# from shapely.geometry import Point
# # import matplotlib.pyplot as plt
# from PIL import Image
# im = Image.open('image.jpg')
# px = im.load()
#
# probit_point = [0.99,0.7,0.3,0.2,0.1]
# probit_dist = [1,2,3,4,5]
#
# # point_x_add = []
# # point_y_add = []
#
# for x in range(11):
#     for y in range(11):
#         dist = round(Point(x,y).distance(Point(1,1)))
#         if dist == 0:
#             px[x, y] = (255, 0, 0)
#         #print('Point: ', x, y, "to point: 1,1", "Distance: ", dist)
#         if dist in probit_dist:
#             find_index = probit_dist.index(dist)
#
#             if probit_point[find_index]>=0.9:
#                 px[x, y] = (255, 0, 0)
#             elif 0.9>probit_point[find_index]>=0.3:
#                 px[x, y] = (255, 255, 0)
#             elif 0.3>probit_point[find_index]>=0:
#                 px[x, y] = (0, 255, 0)
#
#
# im.save('res.png')






# fig, ax = plt.subplots()
# ax.set(xlim=(-1, 10), ylim=(-1, 10))
# ax.scatter(point_x_add, point_y_add,
#            c = 'deeppink')    #  цвет точек
# ax.set_facecolor('black')     #  цвет области Axes
# ax.set_title('Один цвет')     #  заголовок для Axes
#
# fig.set_figwidth(8)     #  ширина и
# fig.set_figheight(8)    #  высота "Figure"
#
# plt.show()
