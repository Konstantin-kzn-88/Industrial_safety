import math
from typing import Any, Union
import os
from datetime import date
from docxtpl import DocxTemplate, InlineImage
from pathlib import Path
from docx.shared import Mm
import numbers
# Мои импортированные классы
from evaporation import class_evaporation_liguid
from event_tree import class_event_tree
from probability import class_probability
from tvs_explosion import class_tvs_explosion
from strait_fire import class_strait_fire
from lower_concentration import class_lower_concentration
from damage import class_damage

TIME_EVAPORATED = 3600  # 3600 секунд, время испарения
MASS_BURNOUT_RATE = 0.06  # массовая скорость выгорания
WIND_VELOCITY = 1  # скорость ветра, м/с
DAMAGE_EXPLOSION = 0.6
DAMAGE_STRAIT = 1
DAMAGE_LCLP = 0.3
DAMAGE_ELIMINATION = 0.1
PART = 0.3


class Device:
    def __init__(self, char_set: dict):
        # Характеристики оборудования
        self.name = char_set["name"]
        self.located = char_set["located"]
        self.material = char_set["material"]
        self.ground = char_set["ground"]
        self.target = char_set["target"]
        self.length = float(char_set["length"])
        self.diameter = float(char_set["diameter"])
        self.pressure = float(char_set["pressure"])
        self.temperature = float(char_set["temperature"])
        self.volume = float(char_set["volume"])
        self.completion = float(char_set["completion"])
        self.spreading = float(char_set["spreading"])
        self.type = int(char_set["type"])
        self.place = float(char_set["place"])
        self.death_person = int(char_set['death_person'])
        self.injured_person = int(char_set['injured_person'])
        # Характеристики вещества
        self.density = float(char_set["density"])
        self.density_gas = float(char_set["density_gas"])
        self.water_cut = float(char_set["water_cut"])
        self.sulfur = float(char_set["sulfur"])
        self.resins = float(char_set["resins"])  # смолы
        self.asphalt = float(char_set["asphalt"])  # асфальтены
        self.paraffin = float(char_set["paraffin"])
        self.viscosity = float(char_set["viscosity"])
        self.hydrogen_sulfide = float(char_set["hydrogen_sulfide"])  # сероводород
        self.molecular_weight = float(char_set["molecular_weight"])
        self.steam_pressure = float(char_set["steam_pressure"])
        self.flash_temperature = float(char_set["flash_temperature"])
        self.boiling_temperature = float(char_set["boiling_temperature"])
        self.class_substance = int(char_set["class_substance"])
        self.view_space = int(char_set["view_space"])
        self.heat_of_combustion = int(char_set["heat_of_combustion"])
        self.sigma = int(char_set["sigma"])
        self.energy_level = int(char_set["energy_level"])
        self.lower_concentration = float(char_set['lower_concentration'])
        self.cost_sub = float(char_set['cost_sub'])
        # Расчетные значения
        self.calc_full()
        self.calc_part()



        self.group_risk = 0
        self.individual_risk = 0

    def calc_full(self):
        # 1. Расчетные значения для полного пролива
        # 1.1. Объем, масса, площадь, количество испарившегося вещества
        self.volume_sub = self.emergency_volume()  # аварийный объем, м3
        self.mass_sub = self.volume_sub * self.density  # аварийная масса выброса, кг
        self.square_sub = self.volume_sub * self.spreading  # аварийная плащодь пролива, м2
        self.evaporated_sub = class_evaporation_liguid.Evapor_liqud().evapor_liguid(self.molecular_weight,
                                                                                    self.steam_pressure,
                                                                                    self.square_sub,
                                                                                    self.mass_sub,
                                                                                    TIME_EVAPORATED)  # количество исп. вещества, кг
        # 1.2.  Сценарии аварии при полном разрушении
        self.probability = class_probability.Probability().probability_rosteh(self.type, self.length)
        self.scenarios_full = class_event_tree.Event_tree().event_tree_inflammable(self.flash_temperature,
                                                                                   0,
                                                                                   self.probability[0]
                                                                                   )
        # 1.3. Расчет зон действия ПФ
        # 1.3.1. Взрыв
        self.explosion_radius = class_tvs_explosion.Explosion().explosion_class_zone(self.class_substance,
                                                                                     self.view_space,
                                                                                     self.evaporated_sub * self.place,
                                                                                     self.heat_of_combustion,
                                                                                     self.sigma,
                                                                                     self.energy_level
                                                                                     )
        # 1.3.2. Пожар пролива
        self.fire_radius = class_strait_fire.Strait_fire().termal_class_zone(self.square_sub,
                                                                             MASS_BURNOUT_RATE,
                                                                             self.molecular_weight,
                                                                             self.boiling_temperature,
                                                                             WIND_VELOCITY
                                                                             )
        # 1.3.3 Пожар вспышка
        self.lclp_radius = class_lower_concentration.LCLP().culculation_R_LCLP(self.evaporated_sub,
                                                                               self.molecular_weight,
                                                                               self.boiling_temperature,
                                                                               self.lower_concentration
                                                                               )
        # 1.4 Ущерб
        self.explosion_damage = class_damage.Damage().damage_array(self.volume * DAMAGE_EXPLOSION,
                                                                   self.diameter,
                                                                   self.length * 1000 * DAMAGE_EXPLOSION,
                                                                   self.cost_sub,
                                                                   DAMAGE_EXPLOSION,
                                                                   self.death_person, self.injured_person,
                                                                   self.evaporated_sub / 1000,
                                                                   self.evaporated_sub / 1000,
                                                                   self.square_sub
                                                                   )

        self.strait_damage = class_damage.Damage().damage_array(self.volume * DAMAGE_STRAIT,
                                                                self.diameter,
                                                                self.length * 1000 * DAMAGE_STRAIT,
                                                                self.cost_sub,
                                                                DAMAGE_STRAIT,
                                                                1, 1,
                                                                self.evaporated_sub / 1000,
                                                                self.mass_sub / 1000,
                                                                self.square_sub
                                                                )

        self.lclp_damage = class_damage.Damage().damage_array(self.volume * DAMAGE_LCLP,
                                                              self.diameter,
                                                              self.length * 1000 * DAMAGE_LCLP,
                                                              self.cost_sub,
                                                              DAMAGE_LCLP,
                                                              1, 1,
                                                              self.evaporated_sub / 1000,
                                                              self.evaporated_sub / 1000,
                                                              self.square_sub
                                                              )

        self.elimination_damage = class_damage.Damage().damage_array(self.volume * DAMAGE_ELIMINATION,
                                                                     self.diameter,
                                                                     self.length * 1000 * DAMAGE_ELIMINATION,
                                                                     self.cost_sub,
                                                                     DAMAGE_ELIMINATION,
                                                                     0, 0,
                                                                     self.evaporated_sub / 1000,
                                                                     0,
                                                                     self.square_sub
                                                                     )
        # 1.5 Риск
        self.explosion_risk = (self.name,
                               "C1",
                               self.scenarios_full[0],
                               self.explosion_damage[-1],
                               "{:.2e}".format(float(self.scenarios_full[0]) * self.explosion_damage[-1]),
                               self.death_person,
                               self.injured_person)

        self.strait_risk = (self.name,
                            "C2",
                            self.scenarios_full[1],
                            self.strait_damage[-1],
                            "{:.2e}".format(float(self.scenarios_full[1]) * self.strait_damage[-1]),
                            1,
                            1)

        self.lslp_risk = (self.name,
                          "C3",
                          self.scenarios_full[2],
                          self.lclp_damage[-1],
                          "{:.2e}".format(float(self.scenarios_full[2]) * self.lclp_damage[-1]),
                          1,
                          1)

        self.elimination_risk = (self.name,
                                 "C4",
                                 self.scenarios_full[3],
                                 self.elimination_damage[-1],
                                 "{:.2e}".format(float(self.scenarios_full[3]) * self.elimination_damage[-1]),
                                 0,
                                 0)

    def calc_part(self):
        # 1. Расчетные значения для частичного пролива
        # 1.1. Объем, масса, площадь, количество испарившегося вещества
        self.volume_sub_part = self.emergency_volume()*PART  # аварийный объем, м3
        self.mass_sub_part = self.volume_sub_part * self.density  # аварийная масса выброса, кг
        self.square_sub_part = self.volume_sub_part * self.spreading  # аварийная плащодь пролива, м2
        self.evaporated_sub_part = class_evaporation_liguid.Evapor_liqud().evapor_liguid(self.molecular_weight,
                                                                                    self.steam_pressure,
                                                                                    self.square_sub_part,
                                                                                    self.mass_sub_part,
                                                                                    TIME_EVAPORATED)  # количество исп. вещества, кг
        # 1.2.  Сценарии аварии при полном разрушении
        self.probability_part = class_probability.Probability().probability_rosteh(self.type, self.length)
        self.scenarios_part = class_event_tree.Event_tree().event_tree_inflammable(self.flash_temperature,
                                                                                   0,
                                                                                   self.probability_part[1]
                                                                                   )
        # 1.3. Расчет зон действия ПФ
        # 1.3.1. Взрыв
        self.explosion_radius_part = class_tvs_explosion.Explosion().explosion_class_zone(self.class_substance,
                                                                                     self.view_space,
                                                                                     self.evaporated_sub_part * self.place,
                                                                                     self.heat_of_combustion,
                                                                                     self.sigma,
                                                                                     self.energy_level
                                                                                     )
        # 1.3.2. Пожар пролива
        self.fire_radius_part = class_strait_fire.Strait_fire().termal_class_zone(self.square_sub_part,
                                                                             MASS_BURNOUT_RATE,
                                                                             self.molecular_weight,
                                                                             self.boiling_temperature,
                                                                             WIND_VELOCITY
                                                                             )
        # 1.3.3 Пожар вспышка
        self.lclp_radius_part = class_lower_concentration.LCLP().culculation_R_LCLP(self.evaporated_sub_part,
                                                                               self.molecular_weight,
                                                                               self.boiling_temperature,
                                                                               self.lower_concentration
                                                                               )
        # 1.4 Ущерб
        self.explosion_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_EXPLOSION*PART,
                                                                   self.diameter,
                                                                   self.length * 1000 * DAMAGE_EXPLOSION*PART,
                                                                   self.cost_sub,
                                                                   DAMAGE_EXPLOSION,
                                                                  0, 1,
                                                                   self.evaporated_sub_part / 1000,
                                                                   self.evaporated_sub_part / 1000,
                                                                   self.square_sub_part
                                                                   )

        self.strait_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_STRAIT*PART,
                                                                self.diameter,
                                                                self.length * 1000 * DAMAGE_STRAIT*PART,
                                                                self.cost_sub,
                                                                DAMAGE_STRAIT,
                                                                0, 1,
                                                                self.evaporated_sub_part / 1000,
                                                                self.mass_sub_part / 1000,
                                                                self.square_sub_part
                                                                )

        self.lclp_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_LCLP*PART,
                                                              self.diameter,
                                                              self.length * 1000 * DAMAGE_LCLP*PART,
                                                              self.cost_sub,
                                                              DAMAGE_LCLP,
                                                              0, 1,
                                                              self.evaporated_sub_part / 1000,
                                                              self.evaporated_sub_part / 1000,
                                                              self.square_sub_part
                                                              )

        self.elimination_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_ELIMINATION*PART,
                                                                     self.diameter,
                                                                     self.length * 1000 * DAMAGE_ELIMINATION*PART,
                                                                     self.cost_sub,
                                                                     DAMAGE_ELIMINATION,
                                                                     0, 0,
                                                                     self.evaporated_sub_part / 1000,
                                                                     0,
                                                                     self.square_sub_part
                                                                     )
        # 1.5 Риск
        self.explosion_risk_part = (self.name,
                               "C1част",
                               self.scenarios_part[0],
                               self.explosion_damage_part[-1],
                               "{:.2e}".format(float(self.scenarios_part[0]) * self.explosion_damage_part[-1]),
                               0,
                               1)

        self.strait_risk_part = (self.name,
                            "C2част",
                            self.scenarios_part[1],
                            self.strait_damage_part[-1],
                            "{:.2e}".format(float(self.scenarios_part[1]) * self.strait_damage_part[-1]),
                            0,
                            1)

        self.lslp_risk_part = (self.name,
                          "C3част",
                          self.scenarios_part[2],
                          self.lclp_damage_part[-1],
                          "{:.2e}".format(float(self.scenarios_part[2]) * self.lclp_damage_part[-1]),
                          1,
                          1)

        self.elimination_risk_part = (self.name,
                                 "C4",
                                 self.scenarios_part[3],
                                 self.elimination_damage_part[-1],
                                 "{:.2e}".format(float(self.scenarios_part[3]) * self.elimination_damage_part[-1]),
                                 0,
                                 0)

    def emergency_volume(self):
        """
        Функция определения аварийного объема для оборудования (максимального), м3
        :return volume - объем, м3
        """
        volume = 0
        if self.length == 0 and self.volume == 0:
            raise ValueError("Объем емкости и длина трубы не могут быть нулевыми одновременно!")
        if self.length != 0 and self.volume != 0:
            raise ValueError("Емкости и трубы не могут быть одновременно заполненными!")
        # Если трубопровод, то есть длина не равно 0
        if self.length != 0:
            volume = math.pi * math.pow(self.diameter / 2000, 2) * (self.length * 1000)
        # Если емкость, то есть объем не равен 0
        if self.volume != 0:
            volume = self.volume * self.completion
        return volume


class Dangerous_object:
    """
    Класс "Опасный объект" предназначен для хранения данных
    об опасном объекте.
    """
    name = "ЗАО «Предприятие Кара Алтын»"
    project = "Обустройствo куста скважин №1063 Тавельского нефтяного месторождения"
    number = "56-20"
    code = "12.1.2"
    description = "Описание работы объекта проектируемого"
    automation = "Автоматизации подлежит то-то и то-то"

    def __init__(self):
        self.list_device = []  # инициализируем пустой список оборудования

    def append_device(self, device: Union[Device]) -> None:
        self.list_device.append(device)


if __name__ == '__main__':
    # 1. Создадим новые объекты
    tube_dict = {
        'name': 'Трубопровод от К-2 до т.вр.12',
        'located': 'Зимнее м.н.',
        'material': 'B20',
        'ground': 'Подземное',
        'target': 'Траспортирование нефти',
        'length': 0.899,  # км
        'diameter': 114,  # мм
        'pressure': 0.24,  # кПа
        'temperature': 30,  # град.С
        'volume': 0,  # м3
        'completion': 1,  # - (степень заполнения)
        'spreading': 20,  # м^-1
        'type': 0,  # тип оборудования
        'place': 0.1,  # коэф.участия во взрыве
        'density': 850,  # кг/м3
        'density_gas': 2,  # кг/м3
        'water_cut': 20,  # %
        'sulfur': 34,  # %
        'resins': 2,  # % смолы
        'asphalt': 3,  # % асфальтены
        'paraffin': 4,  # %
        'viscosity': 220,  # МПа*с
        'hydrogen_sulfide': 32,  # % сероводород
        'molecular_weight': 210,  # кг/кмоль
        'steam_pressure': 28,  # кПа
        'flash_temperature': -28,  # град.С
        'boiling_temperature': -20,  # град.С
        'class_substance': 3,  # класс вещества по детонационной ячейки
        'view_space': 4,  # класс окрущающего пространства
        'heat_of_combustion': 46000,  # кДж/кг
        'sigma': 7,  # -
        'energy_level': 1,  # -
        'lower_concentration': 1.8,
        'cost_sub': 0.06,
        'death_person': 1,
        'injured_person': 2,

    }
    test_tube = Device(tube_dict)
    print(test_tube.volume_sub)
    print(test_tube.mass_sub)
    print(test_tube.square_sub)
    print(test_tube.evaporated_sub)
    print(test_tube.probability)
    print(test_tube.scenarios_full)
    print(test_tube.explosion_radius)
    print(test_tube.fire_radius)
    print(test_tube.lclp_radius)
    print(test_tube.explosion_damage)
    print(test_tube.strait_damage)
    print(test_tube.lclp_damage)
    print(test_tube.elimination_damage)
    print(test_tube.explosion_risk)
    print(test_tube.strait_risk)
    print(test_tube.lslp_risk)
    print(test_tube.elimination_risk)
    print(20*'-')
    print(20 * '-')
    print(test_tube.volume_sub_part)
    print(test_tube.mass_sub_part)
    print(test_tube.square_sub_part)
    print(test_tube.evaporated_sub_part)
    print(test_tube.probability_part)
    print(test_tube.scenarios_part)
    print(test_tube.explosion_radius_part)
    print(test_tube.fire_radius_part)
    print(test_tube.lclp_radius_part)
    print(test_tube.explosion_damage_part)
    print(test_tube.strait_damage_part)
    print(test_tube.lclp_damage_part)
    print(test_tube.elimination_damage_part)
    print(test_tube.explosion_risk_part)
    print(test_tube.strait_risk_part)
    print(test_tube.lslp_risk_part)
    print(test_tube.elimination_risk_part)
