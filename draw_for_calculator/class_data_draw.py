from PySide2 import QtGui
from shapely.geometry import Point, LineString, Polygon
import math
# calc
from evaporation import class_evaporation_liguid
from tvs_explosion import class_tvs_explosion
from strait_fire import class_strait_fire
from lower_concentration import class_lower_concentration
from event_tree import class_event_tree
from probability import class_probability

TIME_EVAPORATED = 3600
MASS_BURNOUT_RATE = 0.06
WIND_VELOCITY = 1


class Data_draw:
    def __init__(self):
        ...

    def data_for_zone(self, data_list: list, plan_report_index: int):
        print("draw zone")
        result = []
        for obj in data_list:
            # a) Посчитаем объем
            length = float(obj[6])
            diameter = float(obj[7])
            volume_char = float(obj[10])  # характеристика емкость, объем, м3
            completion = float(obj[11])
            spill_square = float(obj[12])
            spreading = float(obj[14])
            class_substance = int(obj[22])
            view_space = int(obj[23])
            place = float(obj[15])
            heat_of_combustion = float(obj[24])
            sigma = int(obj[25])
            energy_level = int(obj[26])
            boiling_temperature = float(obj[21])
            lower_concentration = float(obj[28])
            density = float(obj[16])
            molecular_weight = float(obj[18])
            steam_pressure = float(obj[19])
            type = int(obj[13])

            # а. Расчитаем аварийный объем и массу
            volume_sub = 0  # аварийный объем
            # Если трубопровод, то есть длина не равно 0
            if length != 0:
                volume_sub = math.pi * math.pow(diameter / 2000, 2) * (length * 1000)
            # Если емкость, то есть объем не равен 0
            if volume_char != 0:
                volume_sub = volume_char * completion

            mass_sub = volume_sub * density  # аварийная масса выброса, кг

            # б. Определим площадь пролива
            square_sub = (volume_sub * spreading) if spill_square == 0 else spill_square
            # в. Количество испарившегося вещества
            evaporated_sub = class_evaporation_liguid.Evapor_liqud().evapor_liguid(molecular_weight,
                                                                                   steam_pressure,
                                                                                   square_sub,
                                                                                   mass_sub,
                                                                                   TIME_EVAPORATED)  # количество исп. вещества, кг

            # г. Расчет зон действия поражающих факторов
            if plan_report_index == 0:
                explosion_radius = class_tvs_explosion.Explosion().explosion_class_zone(class_substance,
                                                                                        view_space,
                                                                                        evaporated_sub * place,
                                                                                        heat_of_combustion,
                                                                                        sigma,
                                                                                        energy_level
                                                                                        )
                print(explosion_radius)
                result.append(explosion_radius)

            if plan_report_index == 1:
                fire_radius = class_strait_fire.Strait_fire().termal_class_zone(square_sub,
                                                                                MASS_BURNOUT_RATE,
                                                                                molecular_weight,
                                                                                boiling_temperature,
                                                                                WIND_VELOCITY
                                                                                )
                print(fire_radius)
                # Если объект стационарный, то нужно рисовать от края пролива
                # для этого вычтем радиус пролива
                if type != 0:
                    r_eff = math.sqrt(4 * square_sub / math.pi) / 2
                    fire_radius = [i - r_eff for i in fire_radius]

                result.append(fire_radius + ([0] * 2))  # что бы зо было 6 шт.

            if plan_report_index in (2, 3):
                lclp_radius = class_lower_concentration.LCLP().culculation_R_LCLP(evaporated_sub,
                                                                                  molecular_weight,
                                                                                  boiling_temperature,
                                                                                  lower_concentration
                                                                                  )
                print(lclp_radius)
                if plan_report_index == 2:
                    lclp_radius.pop(0)
                    result.append(lclp_radius + ([0] * 5))  # что бы зо было 6 шт.
                if plan_report_index == 3:
                    lclp_radius.pop(1)
                    result.append(lclp_radius + ([0] * 5))  # что бы зо было 6 шт.

        return result

    def data_for_risk(self, data_list: list):

        expl_all_probit = []
        strait_all_probit = []
        flash_all_probit = []
        scenarios_all = []

        for obj in data_list:
            # a) Посчитаем объем
            length = float(obj[6])
            diameter = float(obj[7])
            volume_char = float(obj[10])  # характеристика емкость, объем, м3
            completion = float(obj[11])
            spill_square = float(obj[12])
            spreading = float(obj[14])
            class_substance = int(obj[22])
            view_space = int(obj[23])
            place = float(obj[15])
            heat_of_combustion = float(obj[24])
            sigma = int(obj[25])
            energy_level = int(obj[26])
            boiling_temperature = float(obj[21])
            lower_concentration = float(obj[28])
            density = float(obj[16])
            molecular_weight = float(obj[18])
            steam_pressure = float(obj[19])
            type = int(obj[13])
            flash_temperature = float(obj[20])

            # а. Расчитаем аварийный объем и массу
            volume_sub = 0  # аварийный объем
            # Если трубопровод, то есть длина не равно 0
            if length != 0:
                volume_sub = math.pi * math.pow(diameter / 2000, 2) * (length * 1000)
            # Если емкость, то есть объем не равен 0
            if volume_char != 0:
                volume_sub = volume_char * completion

            mass_sub = volume_sub * density  # аварийная масса выброса, кг

            # б. Определим площадь пролива
            square_sub = (volume_sub * spreading) if spill_square == 0 else spill_square
            # в. Количество испарившегося вещества
            evaporated_sub = class_evaporation_liguid.Evapor_liqud().evapor_liguid(molecular_weight,
                                                                                   steam_pressure,
                                                                                   square_sub,
                                                                                   mass_sub,
                                                                                   TIME_EVAPORATED)  # количество исп. вещества, кг
            # Взрыв
            temp = class_tvs_explosion.Explosion().explosion_array(class_substance,
                                                                   view_space,
                                                                   evaporated_sub * place,
                                                                   heat_of_combustion,
                                                                   sigma,
                                                                   energy_level
                                                                   )

            expl_probit = [temp[0], temp[-1]]  # нужны только радиусы и вероятности поражения
            expl_all_probit.append(expl_probit)
            # Пожар пролива
            temp = class_strait_fire.Strait_fire().termal_radiation_array(square_sub,
                                                                          MASS_BURNOUT_RATE,
                                                                          molecular_weight,
                                                                          boiling_temperature,
                                                                          WIND_VELOCITY
                                                                          )
            strait_probit = [temp[0], temp[-1]]  # нужны только радиусы и вероятности поражения
            strait_all_probit.append(strait_probit)

            temp = class_lower_concentration.LCLP().culculation_R_LCLP(evaporated_sub,
                                                                       molecular_weight,
                                                                       boiling_temperature,
                                                                       lower_concentration
                                                                       )[-1]
            probit = [1 for _ in range(int(temp))]
            radius = [i for i in range(len(probit))]
            flash_probit = [radius, probit]
            flash_all_probit.append(flash_probit)

            # 1.2.  Сценарии аварии при полном разрушении
            probability = class_probability.Probability().probability_rosteh(type, length)
            temp = class_event_tree.Event_tree().event_tree_inflammable(flash_temperature,
                                                                        0, probability[0])

            scenarios_full = [float(i) for i in temp]
            scenarios_all.append(scenarios_full)

        return (expl_all_probit, strait_all_probit, flash_all_probit, scenarios_all)

    def show_heat_map(self, zeors_array, width: int, height: int, qimg_zone):
        max_el = zeors_array.max()

        for x in range(width):
            for y in range(height):
                if zeors_array[x, y] >= max_el:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 0, 0, 255))
                elif max_el * 0.99 > zeors_array[x, y] >= max_el * 0.98:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 10, 0, 255))
                elif max_el * 0.98 > zeors_array[x, y] >= max_el * 0.97:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 20, 0, 255))
                elif max_el * 0.97 > zeors_array[x, y] >= max_el * 0.96:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 30, 0, 255))
                elif max_el * 0.96 > zeors_array[x, y] >= max_el * 0.95:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 40, 0, 255))
                elif max_el * 0.95 > zeors_array[x, y] >= max_el * 0.94:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 50, 0, 255))
                elif max_el * 0.94 > zeors_array[x, y] >= max_el * 0.93:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 60, 0, 255))
                elif max_el * 0.93 > zeors_array[x, y] >= max_el * 0.92:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 70, 0, 255))
                elif max_el * 0.92 > zeors_array[x, y] >= max_el * 0.91:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 80, 0, 255))
                elif max_el * 0.91 > zeors_array[x, y] >= max_el * 0.90:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 90, 0, 255))
                elif max_el * 0.90 > zeors_array[x, y] >= max_el * 0.89:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 100, 0, 255))
                elif max_el * 0.89 > zeors_array[x, y] >= max_el * 0.88:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 110, 0, 255))
                elif max_el * 0.88 > zeors_array[x, y] >= max_el * 0.87:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 120, 0, 255))
                elif max_el * 0.87 > zeors_array[x, y] >= max_el * 0.86:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 130, 0, 255))
                elif max_el * 0.86 > zeors_array[x, y] >= max_el * 0.85:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 140, 0, 255))
                elif max_el * 0.85 > zeors_array[x, y] >= max_el * 0.84:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 150, 0, 255))
                elif max_el * 0.84 > zeors_array[x, y] >= max_el * 0.83:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 160, 0, 255))
                elif max_el * 0.83 > zeors_array[x, y] >= max_el * 0.82:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 170, 0, 255))
                elif max_el * 0.82 > zeors_array[x, y] >= max_el * 0.81:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 180, 0, 255))
                elif max_el * 0.81 > zeors_array[x, y] >= max_el * 0.80:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 190, 0, 255))
                elif max_el * 0.80 > zeors_array[x, y] >= max_el * 0.79:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 200, 0, 255))
                elif max_el * 0.79 > zeors_array[x, y] >= max_el * 0.78:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 210, 0, 255))
                elif max_el * 0.78 > zeors_array[x, y] >= max_el * 0.77:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 220, 0, 255))
                elif max_el * 0.77 > zeors_array[x, y] >= max_el * 0.76:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 230, 0, 255))
                elif max_el * 0.76 > zeors_array[x, y] >= max_el * 0.75:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 240, 0, 255))
                elif max_el * 0.75 > zeors_array[x, y] >= max_el * 0.74:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(255, 255, 0, 255))
                elif max_el * 0.74 > zeors_array[x, y] >= max_el * 0.73:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(240, 255, 0, 255))
                elif max_el * 0.73 > zeors_array[x, y] >= max_el * 0.72:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(230, 255, 0, 255))
                elif max_el * 0.72 > zeors_array[x, y] >= max_el * 0.71:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(220, 255, 0, 255))
                elif max_el * 0.71 > zeors_array[x, y] >= max_el * 0.70:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(210, 255, 0, 255))
                elif max_el * 0.70 > zeors_array[x, y] >= max_el * 0.69:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(200, 255, 0, 255))
                elif max_el * 0.69 > zeors_array[x, y] >= max_el * 0.68:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(190, 255, 0, 255))
                elif max_el * 0.68 > zeors_array[x, y] >= max_el * 0.67:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(180, 255, 0, 255))
                elif max_el * 0.67 > zeors_array[x, y] >= max_el * 0.66:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(170, 255, 0, 255))
                elif max_el * 0.66 > zeors_array[x, y] >= max_el * 0.65:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(160, 255, 0, 255))
                elif max_el * 0.65 > zeors_array[x, y] >= max_el * 0.64:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(150, 255, 0, 255))
                elif max_el * 0.64 > zeors_array[x, y] >= max_el * 0.63:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(140, 255, 0, 255))
                elif max_el * 0.63 > zeors_array[x, y] >= max_el * 0.62:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(130, 255, 0, 255))
                elif max_el * 0.62 > zeors_array[x, y] >= max_el * 0.61:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(120, 255, 0, 255))
                elif max_el * 0.61 > zeors_array[x, y] >= max_el * 0.60:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(110, 255, 0, 255))
                elif max_el * 0.60 > zeors_array[x, y] >= max_el * 0.59:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(100, 255, 0, 255))
                elif max_el * 0.59 > zeors_array[x, y] >= max_el * 0.58:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(90, 255, 0, 255))
                elif max_el * 0.58 > zeors_array[x, y] >= max_el * 0.57:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(80, 255, 0, 255))
                elif max_el * 0.57 > zeors_array[x, y] >= max_el * 0.56:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(70, 255, 0, 255))
                elif max_el * 0.56 > zeors_array[x, y] >= max_el * 0.55:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(60, 255, 0, 255))
                elif max_el * 0.55 > zeors_array[x, y] >= max_el * 0.54:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(50, 255, 0, 255))
                elif max_el * 0.54 > zeors_array[x, y] >= max_el * 0.53:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(40, 255, 0, 255))
                elif max_el * 0.53 > zeors_array[x, y] >= max_el * 0.52:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(30, 255, 0, 255))
                elif max_el * 0.52 > zeors_array[x, y] >= max_el * 0.51:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(20, 255, 0, 255))
                elif max_el * 0.51 > zeors_array[x, y] >= max_el * 0.50:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(10, 255, 0, 255))
                elif max_el * 0.50 > zeors_array[x, y] >= max_el * 0.49:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 255, 0, 255))
                elif max_el * 0.49 > zeors_array[x, y] >= max_el * 0.48:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 235, 255, 255))
                elif max_el * 0.48 > zeors_array[x, y] >= max_el * 0.47:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 235, 255, 255))
                elif max_el * 0.47 > zeors_array[x, y] >= max_el * 0.46:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 225, 255, 255))
                elif max_el * 0.46 > zeors_array[x, y] >= max_el * 0.45:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 215, 255, 255))
                elif max_el * 0.45 > zeors_array[x, y] >= max_el * 0.44:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 205, 255, 255))
                elif max_el * 0.44 > zeors_array[x, y] >= max_el * 0.43:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 195, 255, 255))
                elif max_el * 0.43 > zeors_array[x, y] >= max_el * 0.42:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 185, 255, 255))
                elif max_el * 0.42 > zeors_array[x, y] >= max_el * 0.41:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 175, 255, 255))
                elif max_el * 0.41 > zeors_array[x, y] >= max_el * 0.40:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 165, 255, 255))
                elif max_el * 0.40 > zeors_array[x, y] >= max_el * 0.39:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 155, 255, 255))
                elif max_el * 0.39 > zeors_array[x, y] >= max_el * 0.38:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 145, 255, 255))
                elif max_el * 0.38 > zeors_array[x, y] >= max_el * 0.37:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 135, 255, 255))
                elif max_el * 0.37 > zeors_array[x, y] >= max_el * 0.36:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 125, 255, 255))
                elif max_el * 0.36 > zeors_array[x, y] >= max_el * 0.35:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 115, 255, 255))
                elif max_el * 0.35 > zeors_array[x, y] >= max_el * 0.34:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 105, 255, 255))
                elif max_el * 0.34 > zeors_array[x, y] >= max_el * 0.33:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 95, 255, 255))
                elif max_el * 0.33 > zeors_array[x, y] >= max_el * 0.32:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 85, 255, 255))
                elif max_el * 0.32 > zeors_array[x, y] >= max_el * 0.31:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 75, 255, 255))
                elif max_el * 0.31 > zeors_array[x, y] >= max_el * 0.30:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 65, 255, 255))
                elif max_el * 0.30 > zeors_array[x, y] >= max_el * 0.29:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 55, 255, 255))
                elif max_el * 0.29 > zeors_array[x, y] >= max_el * 0.28:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 45, 255, 255))
                elif max_el * 0.28 > zeors_array[x, y] >= max_el * 0.27:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 35, 255, 255))
                elif max_el * 0.27 > zeors_array[x, y] >= max_el * 0.26:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 25, 255, 255))
                elif max_el * 0.26 > zeors_array[x, y] >= max_el * 0.25:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 25, 255, 255))
                elif max_el * 0.25 > zeors_array[x, y] >= max_el * 0.01:
                    qimg_zone.setPixelColor(x, y, QtGui.QColor(0, 0, 255, 255))

        return qimg_zone

    def calc_heat_map(self, sharpness: int, zeors_array, data_list: list, width: int, height: int, scale_plan: float,
                      expl_all_probit: list, strait_all_probit: list, flash_all_probit: list, scenarios_all: list):

        # Вспомогательные функции
        def fast_calc(x, y, sharpness):
            for i in range(x - sharpness, x):
                for j in range(y - sharpness, y):
                    zeors_array[i, j] = zeors_array[x, y]

        def get_polyline_shapely(coordinate):

            i = 0
            points = []
            while i < len(coordinate):
                point = (int(float(coordinate[i])), int(float(coordinate[i + 1])))
                points.append(point)
                i += 2
            polyline = LineString(points)

            return polyline

        def get_polygon_shapely(coordinate):

            i = 0
            points = []
            while i < len(coordinate):
                point = (int(float(coordinate[i])), int(float(coordinate[i + 1])))
                points.append(point)
                i += 2
            polygon = Polygon(points)

            return polygon

        for x in range(sharpness, width, sharpness):
            for y in range(sharpness, height, sharpness):
                # определим расстояние до каждого объекта
                for obj in data_list:
                    coordinate = list(map(float, eval(obj[-1])))
                    type = int(obj[13])
                    # рассчтоние от точки до объекта с учетом его типа
                    # если трубопровод, то как до линии
                    if len(coordinate) > 2:  # координаты можно преобразовать в полигон или линию
                        if type == 0:
                            # линейн. получим полигон
                            obj_coord = get_polyline_shapely(coordinate)
                            distance = int(round(Point(x, y).distance(obj_coord) * scale_plan))
                        else:
                            # стац. об. получим полигон
                            obj_coord = get_polygon_shapely(coordinate)
                            distance = int(round(Point(x, y).distance(obj_coord) * scale_plan))
                    else:  # не получается полигон, значит точка
                        obj_coord = Point(float(coordinate[0]), float(coordinate[1]))
                        distance = int(round(Point(x, y).distance(obj_coord) * scale_plan))
                    # Найдем нужный пробит
                    # 1. Индекс объекта в списке
                    ind = data_list.index(obj)
                    # 2. Возьмем пробит-массив по индексу
                    expl_raduis = expl_all_probit[ind][0]
                    strait_raduis = strait_all_probit[ind][0]
                    flash_raduis = flash_all_probit[ind][0]
                    # 3. Определим есть ли в нем расстояние
                    # 3.1 Взрыв
                    if distance in expl_raduis:
                        zeors_array[x, y] = zeors_array[x, y] + expl_all_probit[ind][1][expl_raduis.index(distance)] * \
                                            scenarios_all[ind][0]
                        fast_calc(x, y, sharpness)
                    elif distance == 0:
                        zeors_array[x, y] = zeors_array[x, y] + max(expl_all_probit[ind][1]) * scenarios_all[ind][0]
                        fast_calc(x, y, sharpness)
                    # 3.2 Пожар
                    if distance in strait_raduis:
                        # если есть дисктанция в радиусах взрыва объекта
                        zeors_array[x, y] = zeors_array[x, y] + strait_all_probit[ind][1][
                            strait_raduis.index(distance)] * scenarios_all[ind][1]
                        fast_calc(x, y, sharpness)
                    elif distance == 0:
                        zeors_array[x, y] = zeors_array[x, y] + max(strait_all_probit[ind][1]) * scenarios_all[ind][1]
                        fast_calc(x, y, sharpness)

                    # 3.3 Вспышка
                    if distance in flash_raduis:
                        # если есть дисктанция в радиусах взрыва объекта
                        zeors_array[x, y] = zeors_array[x, y] + flash_all_probit[ind][1][flash_raduis.index(distance)] * \
                                            scenarios_all[ind][2]
                        fast_calc(x, y, sharpness)
                    elif distance == 0:
                        zeors_array[x, y] = zeors_array[x, y] + max(flash_all_probit[ind][1]) * scenarios_all[ind][2]
                        fast_calc(x, y, sharpness)

        return zeors_array
