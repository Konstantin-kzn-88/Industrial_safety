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
        self.name_full = char_set['name_full']
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
        self.time_person = float(char_set['time_person'])
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

        self.group_risk, self.individual_risk = self.calc_risk()

    def calc_risk(self):
        group_risk = 0
        list_people = [self.death_person, 1, 1, 0]
        for i in range(len(self.scenarios_full)):
            group_risk += float(self.scenarios_full[i]) * list_people[i]
        individual_risk = "{:.2e}".format((group_risk / sum(list_people)) * self.time_person)
        group_risk = "{:.2e}".format(group_risk)

        return group_risk, individual_risk

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
                                                                   1, 1,
                                                                   self.evaporated_sub / 1000,
                                                                   self.evaporated_sub / 1000,
                                                                   self.square_sub
                                                                   )

        self.strait_damage = class_damage.Damage().damage_array(self.volume * DAMAGE_STRAIT,
                                                                self.diameter,
                                                                self.length * 1000 * DAMAGE_STRAIT,
                                                                self.cost_sub,
                                                                DAMAGE_STRAIT,
                                                                self.death_person, self.injured_person,
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
                               1,
                               1)

        self.strait_risk = (self.name,
                            "C2",
                            self.scenarios_full[1],
                            self.strait_damage[-1],
                            "{:.2e}".format(float(self.scenarios_full[1]) * self.strait_damage[-1]),
                            self.death_person,
                            self.injured_person)

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
        self.volume_sub_part = self.emergency_volume() * PART  # аварийный объем, м3
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
        self.explosion_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_EXPLOSION * PART,
                                                                        self.diameter,
                                                                        self.length * 1000 * DAMAGE_EXPLOSION * PART,
                                                                        self.cost_sub,
                                                                        DAMAGE_EXPLOSION,
                                                                        0, 1,
                                                                        self.evaporated_sub_part / 1000,
                                                                        self.evaporated_sub_part / 1000,
                                                                        self.square_sub_part
                                                                        )

        self.strait_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_STRAIT * PART,
                                                                     self.diameter,
                                                                     self.length * 1000 * DAMAGE_STRAIT * PART,
                                                                     self.cost_sub,
                                                                     DAMAGE_STRAIT,
                                                                     0, 1,
                                                                     self.evaporated_sub_part / 1000,
                                                                     self.mass_sub_part / 1000,
                                                                     self.square_sub_part
                                                                     )

        self.lclp_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_LCLP * PART,
                                                                   self.diameter,
                                                                   self.length * 1000 * DAMAGE_LCLP * PART,
                                                                   self.cost_sub,
                                                                   DAMAGE_LCLP,
                                                                   0, 1,
                                                                   self.evaporated_sub_part / 1000,
                                                                   self.evaporated_sub_part / 1000,
                                                                   self.square_sub_part
                                                                   )

        self.elimination_damage_part = class_damage.Damage().damage_array(self.volume * DAMAGE_ELIMINATION * PART,
                                                                          self.diameter,
                                                                          self.length * 1000 * DAMAGE_ELIMINATION * PART,
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
                               0,
                               1)

        self.elimination_risk_part = (self.name,
                                      "C4част",
                                      self.scenarios_part[3],
                                      self.elimination_damage_part[-1],
                                      "{:.2e}".format(float(self.scenarios_part[3]) * self.elimination_damage_part[-1]),
                                      0,
                                      0)
        print(self.explosion_risk_part)
        print(self.strait_risk_part)
        print(self.lslp_risk_part)
        print(self.elimination_risk_part)

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

    def __init__(self):
        self.name = "ЗАО «Предприятие Кара Алтын»"
        self.project = "Обустройствo куста скважин №1063 Тавельского нефтяного месторождения"
        self.number = "56-20"
        self.code = "12.1.2"
        self.description = "Описание работы объекта проектируемого"
        self.automation = "Автоматизации подлежит то-то и то-то"
        self.list_device = []  # инициализируем пустой список оборудования

    def append_device(self, device: Union[Device]) -> None:
        self.list_device.append(device)

    def create_rpz(self):
        def equipment():
            # Оборудование
            pozitions = [i.name for i in self.list_device]

            name_equps = [f'{i.name_full}, {i.material}' for i in self.list_device]

            locations = [i.ground for i in self.list_device]

            numbers = ["1" for _ in range(0, len(pozitions))]

            appointments = [i.target for i in self.list_device]

            characteristics = []
            for item in self.list_device:
                if item.volume == 0:
                    app_str = f'L = {item.length} км;\nDвн = {item.diameter} мм;\nPн = {item.pressure} МПа'
                    characteristics.append(app_str)
                if item.length == 0:
                    app_str = f'V = {item.volume} м3;\na = {item.completion} -;\nP = {item.pressure} МПа'
                    characteristics.append(app_str)

            equp_table = [{'pozition': pozition, 'name_equp': name_equp, 'location': location, 'number': number,
                           'appointment': appointment, 'characteristic': characteristic}
                          for pozition, name_equp, location, number, appointment, characteristic in
                          zip(pozitions, name_equps, locations, numbers, appointments, characteristics)]
            return equp_table

        def mass_in_equipment():
            # Распредление опасного вещества
            components = [i.located for i in self.list_device]

            pozitions_with_sub = [i.name + ', нефть' for i in self.list_device]

            lenghts_or_num = [(str(i.length) + " км") if i.type == 0 else 1 for i in self.list_device]

            quantitis = [round(i.mass_sub / 1000, 2) for i in self.list_device]

            states = ['Ж.ф.' if i.type == 0 else 'Ж.ф.+п.г.ф.' for i in self.list_device]

            pressures = [i.pressure for i in self.list_device]

            temperatures = [i.temperature for i in self.list_device]

            mass_sub_table = [
                {'component': component, 'pozition_with_sub': pozition_with_sub, 'lenght_or_num': lenght_or_num,
                 'quantity': quantity,
                 'state': state, 'pressure': pressure, 'temperature': temperature}
                for component, pozition_with_sub, lenght_or_num, quantity, state, pressure, temperature in
                zip(components, pozitions_with_sub, lenghts_or_num, quantitis, states, pressures, temperatures)]
            return mass_sub_table

        def mass_crash():
            scenarios = ["C1", "C2", "C3", "C4"] * len(self.list_device)
            name_equps = []
            frequencis = []
            sub_mass_alls = []
            sub_mass_parts = []
            for item in self.list_device:
                for add_fr in item.scenarios_full:
                    frequencis.append(add_fr)
                sub_mass_alls.extend([round(item.mass_sub, 2) for _ in range(4)])
                sub_mass_parts.extend([round(item.mass_sub, 2), round(item.evaporated_sub, 2),
                                       round(item.mass_sub, 2), "-"])
                name_equps.extend([item.name for _ in range(4)])

            effects = ['Термический ожог',
                       'Избыточное давление',
                       'Термический ожог',
                       'Загрязнение окружающей среды'] * len(scenarios)

            mass_crash_table = [{'scenario': scenario, 'name_equp': name_equp, 'frequency': frequency,
                                 'effect': effect, 'sub_mass_all': sub_mass_all, 'sub_mass_part': sub_mass_part}
                                for scenario, name_equp, frequency, effect, sub_mass_all, sub_mass_part in
                                zip(scenarios, name_equps, frequencis, effects, sub_mass_alls,
                                    sub_mass_parts)]

            return mass_crash_table

        def mass_crash_part():
            scenarios_part = ["C1_1", "C2_1", "C3_1", "C4_1"] * len(self.list_device)
            name_equps_part = []
            frequencis_part = []
            sub_mass_alls_part = []
            sub_mass_parts_part = []
            for item in self.list_device:
                for add_fr in item.scenarios_part:
                    frequencis_part.append(add_fr)
                sub_mass_alls_part.extend([round(item.mass_sub_part, 2) for _ in range(4)])
                sub_mass_parts_part.extend([round(item.mass_sub_part, 2), round(item.evaporated_sub_part, 2),
                                            round(item.mass_sub_part, 2), "-"])
                name_equps_part.extend([item.name for _ in range(4)])

            effects_part = ['Термический ожог',
                            'Избыточное давление',
                            'Термический ожог',
                            'Загрязнение окружающей среды'] * len(scenarios_part)

            mass_crash_table_part = [
                {'scenario_part': scenario_part, 'name_equp_part': name_equp_part, 'frequency_part': frequency_part,
                 'effect_part': effect_part, 'sub_mass_all_part': sub_mass_all_part,
                 'sub_mass_part_part': sub_mass_part_part}
                for scenario_part, name_equp_part, frequency_part, effect_part, sub_mass_all_part, sub_mass_part_part in
                zip(scenarios_part, name_equps_part, frequencis_part, effects_part, sub_mass_alls_part,
                    sub_mass_parts_part)]

            return mass_crash_table_part

        def most_dangerous():
            spill = 0
            res = ""
            for item in self.list_device:
                if item.square_sub > spill:
                    res = f'сценарий С1 (пожар пролива) для оборудования "{item.name}" с вероятностью {item.scenarios_full[0]}.'
                spill = item.square_sub
            return res

        def most_possible():
            res = 0
            scenarios = 0
            for item in self.list_device:
                if float(item.scenarios_part[-1]) > scenarios:
                    res = f'сценарий С4_1 (частичная разгерметизация с ликвидацией пролива пролива) для оборудования "{item.name}" с вероятностью {item.scenarios_part[-1]}.'
                scenarios = float(item.scenarios_part[-1])
            return res

        def explosion_crash():

            scenarios_C2 = ["C2"] * len(self.list_device)

            name_equps = []
            sub_masses_C2 = []
            heats_C2 = []
            pressures_100 = []
            pressures_53 = []
            pressures_28 = []
            pressures_12 = []
            pressures_5 = []
            pressures_3 = []
            men_C2 = []

            for item in self.list_device:
                name_equps.append(item.name)
                sub_masses_C2.append(round(item.evaporated_sub, 2))
                heats_C2.append(item.heat_of_combustion)
                pressures_100.append(item.explosion_radius[0])
                pressures_53.append(item.explosion_radius[1])
                pressures_28.append(item.explosion_radius[2])
                pressures_12.append(item.explosion_radius[3])
                pressures_5.append(item.explosion_radius[4])
                pressures_3.append(item.explosion_radius[5])
                men_C2.append('1/1')

            C2_table_factor = [
                {'scenario_C2': scenario_C2, 'name_equp': name_equp, 'sub_mass_C2': sub_mass_C2, 'heat_C2': heat_C2,
                 'dp_100': dp_100, 'dp_53': dp_53, 'dp_28': dp_28,
                 'dp_12': dp_12, 'dp_5': dp_5, 'dp_3': dp_3, 'people_C2': people_C2}
                for
                scenario_C2, name_equp, sub_mass_C2, heat_C2, dp_100, dp_53, dp_28, dp_12, dp_5, dp_3, people_C2
                in
                zip(scenarios_C2, name_equps, sub_masses_C2, heats_C2, pressures_100, pressures_53,
                    pressures_28, pressures_12, pressures_5, pressures_3, men_C2)]

            return C2_table_factor

        def explosion_crash_part():

            scenarios_C2 = ["C2_1"] * len(self.list_device)

            name_equps = []
            sub_masses_C2 = []
            heats_C2 = []
            pressures_100 = []
            pressures_53 = []
            pressures_28 = []
            pressures_12 = []
            pressures_5 = []
            pressures_3 = []
            men_C2 = []

            for item in self.list_device:
                name_equps.append(item.name)
                sub_masses_C2.append(round(item.evaporated_sub_part, 2))
                heats_C2.append(item.heat_of_combustion)
                pressures_100.append(item.explosion_radius_part[0])
                pressures_53.append(item.explosion_radius_part[1])
                pressures_28.append(item.explosion_radius_part[2])
                pressures_12.append(item.explosion_radius_part[3])
                pressures_5.append(item.explosion_radius_part[4])
                pressures_3.append(item.explosion_radius_part[5])
                men_C2.append('0/1')

            C2_table_factor_part = [
                {'scenario_C2': scenario_C2, 'name_equp': name_equp, 'sub_mass_C2': sub_mass_C2, 'heat_C2': heat_C2,
                 'dp_100': dp_100, 'dp_53': dp_53, 'dp_28': dp_28,
                 'dp_12': dp_12, 'dp_5': dp_5, 'dp_3': dp_3, 'people_C2': people_C2}
                for
                scenario_C2, name_equp, sub_mass_C2, heat_C2, dp_100, dp_53, dp_28, dp_12, dp_5, dp_3, people_C2
                in
                zip(scenarios_C2, name_equps, sub_masses_C2, heats_C2, pressures_100, pressures_53,
                    pressures_28, pressures_12, pressures_5, pressures_3, men_C2)]

            return C2_table_factor_part

        def fire_crash():
            # таблица пожаров
            scenarios_C1 = ["C1"] * len(self.list_device)
            name_equps = []
            squares_C1 = []
            intensitis_10 = []
            intensitis_7 = []
            intensitis_4 = []
            intensitis_1 = []
            men_C1 = []
            for item in self.list_device:
                name_equps.append(item.name)
                squares_C1.append(round(item.square_sub, 2))
                intensitis_10.append(item.fire_radius[0])
                intensitis_7.append(item.fire_radius[1])
                intensitis_4.append(item.fire_radius[2])
                intensitis_1.append(item.fire_radius[3])
                men_C1.append(f'{item.death_person}/{item.injured_person}')

            C1_table_factor = [{'scenario_C1': scenario_C1, 'name_equp': name_equp, 'square_C1': square_C1,
                                'q_10': q_10, 'q_7': q_7, 'q_4': q_4, 'q_1': q_1, 'people_C1': people_C1}
                               for
                               scenario_C1, name_equp, square_C1, q_10, q_7, q_4, q_1, people_C1
                               in
                               zip(scenarios_C1, name_equps, squares_C1, intensitis_10,
                                   intensitis_7, intensitis_4, intensitis_1, men_C1)]

            return C1_table_factor

        def fire_crash_part():
            # таблица пожаров
            scenarios_C1 = ["C1_1"] * len(self.list_device)
            name_equps = []
            squares_C1 = []
            intensitis_10 = []
            intensitis_7 = []
            intensitis_4 = []
            intensitis_1 = []
            men_C1 = []
            for item in self.list_device:
                name_equps.append(item.name)
                squares_C1.append(round(item.square_sub_part, 2))
                intensitis_10.append(item.fire_radius_part[0])
                intensitis_7.append(item.fire_radius_part[1])
                intensitis_4.append(item.fire_radius_part[2])
                intensitis_1.append(item.fire_radius_part[3])
                men_C1.append(f'0/1')

            C1_table_factor_part = [{'scenario_C1': scenario_C1, 'name_equp': name_equp, 'square_C1': square_C1,
                                     'q_10': q_10, 'q_7': q_7, 'q_4': q_4, 'q_1': q_1, 'people_C1': people_C1}
                                    for
                                    scenario_C1, name_equp, square_C1, q_10, q_7, q_4, q_1, people_C1
                                    in
                                    zip(scenarios_C1, name_equps, squares_C1, intensitis_10,
                                        intensitis_7, intensitis_4, intensitis_1, men_C1)]

            return C1_table_factor_part

        def lclp_crash():
            # таблица вспышек
            scenarios_C3 = ["C3"] * len(self.list_device)
            name_equps = []
            sub_masses_C3 = []
            heats_C3 = []
            radiuses_nkpr_C3 = []
            radiuses_vsp_C3 = []
            men_C3 = []

            for item in self.list_device:
                name_equps.append(item.name)
                sub_masses_C3.append(round(item.evaporated_sub, 2))
                heats_C3.append(item.heat_of_combustion)
                radiuses_nkpr_C3.append(item.lclp_radius[0])
                radiuses_vsp_C3.append(item.lclp_radius[1])
                men_C3.append('1/1')

            C3_table_factor = [
                {'scenario_C3': scenario_C3, 'name_equp': name_equp, 'sub_mass_C3': sub_mass_C3, 'heat_C3': heat_C3,
                 'radius_nkpr_C3': radius_nkpr_C3, 'radius_vsp_C3': radius_vsp_C3,
                 'people_C3': people_C3}
                for
                scenario_C3, name_equp, sub_mass_C3, heat_C3, radius_nkpr_C3, radius_vsp_C3, people_C3 in
                zip(scenarios_C3, name_equps, sub_masses_C3, heats_C3, radiuses_nkpr_C3, radiuses_vsp_C3, men_C3)]

            return C3_table_factor

        def lclp_crash_part():
            # таблица вспышек
            scenarios_C3 = ["C3_1"] * len(self.list_device)
            name_equps = []
            sub_masses_C3 = []
            heats_C3 = []
            radiuses_nkpr_C3 = []
            radiuses_vsp_C3 = []
            men_C3 = []

            for item in self.list_device:
                name_equps.append(item.name)
                sub_masses_C3.append(round(item.evaporated_sub_part, 2))
                heats_C3.append(item.heat_of_combustion)
                radiuses_nkpr_C3.append(item.lclp_radius_part[0])
                radiuses_vsp_C3.append(item.lclp_radius_part[1])
                men_C3.append('0/1')

            C3_table_factor_part = [
                {'scenario_C3': scenario_C3, 'name_equp': name_equp, 'sub_mass_C3': sub_mass_C3, 'heat_C3': heat_C3,
                 'radius_nkpr_C3': radius_nkpr_C3, 'radius_vsp_C3': radius_vsp_C3,
                 'people_C3': people_C3}
                for
                scenario_C3, name_equp, sub_mass_C3, heat_C3, radius_nkpr_C3, radius_vsp_C3, people_C3 in
                zip(scenarios_C3, name_equps, sub_masses_C3, heats_C3, radiuses_nkpr_C3, radiuses_vsp_C3, men_C3)]

            return C3_table_factor_part

        def damage():
            # таблица ущерба
            scenarios_damage = ["C1", "C2", "C3", "C4"] * len(self.list_device)
            name_equps = []
            straights = []
            localizations = []
            economics = []
            works = []
            indirects = []
            ecologys = []
            sums_damage = []

            for item in self.list_device:
                name_equps.extend([item.name for _ in range(4)])
                straights.append(item.strait_damage[0])
                localizations.append(item.strait_damage[1])
                economics.append(item.strait_damage[2])
                works.append(item.strait_damage[8])
                indirects.append(item.strait_damage[3])
                ecologys.append(item.strait_damage[7])
                sums_damage.append(item.strait_damage[9])

                straights.append(item.explosion_damage[0])
                localizations.append(item.explosion_damage[1])
                economics.append(item.explosion_damage[2])
                works.append(item.explosion_damage[8])
                indirects.append(item.explosion_damage[3])
                ecologys.append(item.explosion_damage[7])
                sums_damage.append(item.explosion_damage[9])

                straights.append(item.lclp_damage[0])
                localizations.append(item.lclp_damage[1])
                economics.append(item.lclp_damage[2])
                works.append(item.lclp_damage[8])
                indirects.append(item.lclp_damage[3])
                ecologys.append(item.lclp_damage[7])
                sums_damage.append(item.lclp_damage[9])

                straights.append(item.elimination_damage[0])
                localizations.append(item.elimination_damage[1])
                economics.append(item.elimination_damage[2])
                works.append(item.elimination_damage[8])
                indirects.append(item.elimination_damage[3])
                ecologys.append(item.elimination_damage[7])
                sums_damage.append(item.elimination_damage[9])

            damage_table = [{'scenario_damage': scenario_damage, 'name_equp': name_equp, 'straight': straight,
                             'localization': localization,
                             'economic': economic, 'work': work, 'indirect': indirect, 'ecology': ecology,
                             'sum_damage': sum_damage}
                            for
                            scenario_damage, name_equp, straight, localization, economic, work, indirect, ecology, sum_damage
                            in
                            zip(scenarios_damage, name_equps, straights, localizations, economics, works, indirects,
                                ecologys,
                                sums_damage)]

            return damage_table

        def damage_part():
            # таблица ущерба
            scenarios_damage = ["C1_1", "C2_1", "C3_1", "C4_1"] * len(self.list_device)
            name_equps = []
            straights = []
            localizations = []
            economics = []
            works = []
            indirects = []
            ecologys = []
            sums_damage = []

            for item in self.list_device:
                name_equps.extend([item.name for _ in range(4)])
                straights.append(item.strait_damage_part[0])
                localizations.append(item.strait_damage_part[1])
                economics.append(item.strait_damage_part[2])
                works.append(item.strait_damage_part[8])
                indirects.append(item.strait_damage_part[3])
                ecologys.append(item.strait_damage_part[7])
                sums_damage.append(item.strait_damage_part[9])

                straights.append(item.explosion_damage_part[0])
                localizations.append(item.explosion_damage_part[1])
                economics.append(item.explosion_damage_part[2])
                works.append(item.explosion_damage_part[8])
                indirects.append(item.explosion_damage_part[3])
                ecologys.append(item.explosion_damage_part[7])
                sums_damage.append(item.explosion_damage_part[9])

                straights.append(item.lclp_damage_part[0])
                localizations.append(item.lclp_damage_part[1])
                economics.append(item.lclp_damage_part[2])
                works.append(item.lclp_damage_part[8])
                indirects.append(item.lclp_damage_part[3])
                ecologys.append(item.lclp_damage_part[7])
                sums_damage.append(item.lclp_damage_part[9])

                straights.append(item.elimination_damage_part[0])
                localizations.append(item.elimination_damage_part[1])
                economics.append(item.elimination_damage_part[2])
                works.append(item.elimination_damage_part[8])
                indirects.append(item.elimination_damage_part[3])
                ecologys.append(item.elimination_damage_part[7])
                sums_damage.append(item.elimination_damage_part[9])

            damage_table_part = [{'scenario_damage': scenario_damage, 'name_equp': name_equp, 'straight': straight,
                                  'localization': localization,
                                  'economic': economic, 'work': work, 'indirect': indirect, 'ecology': ecology,
                                  'sum_damage': sum_damage}
                                 for
                                 scenario_damage, name_equp, straight, localization, economic, work, indirect, ecology, sum_damage
                                 in
                                 zip(scenarios_damage, name_equps, straights, localizations, economics, works,
                                     indirects, ecologys,
                                     sums_damage)]

            return damage_table_part

        def math_risk():
            # таблица результатов расчета риска
            scenarios_risk = ["C1", "C2", "C3", "C4"] * len(self.list_device)
            name_equps =[]
            frequencies_risk = []
            sums_damage_risk = []
            maths_expectation = []
            men_dead = []
            men_injured = []

            for item in self.list_device:
                name_equps.extend([item.name for _ in range(4)])
                frequencies_risk.append(item.explosion_risk[2])
                sums_damage_risk.append(item.explosion_risk[3])
                maths_expectation.append(item.explosion_risk[4])
                men_dead.append(item.explosion_risk[5])
                men_injured.append(item.explosion_risk[6])

                frequencies_risk.append(item.strait_risk[2])
                sums_damage_risk.append(item.strait_risk[3])
                maths_expectation.append(item.strait_risk[4])
                men_dead.append(item.strait_risk[5])
                men_injured.append(item.strait_risk[6])

                frequencies_risk.append(item.lslp_risk[2])
                sums_damage_risk.append(item.lslp_risk[3])
                maths_expectation.append(item.lslp_risk[4])
                men_dead.append(item.lslp_risk[5])
                men_injured.append(item.lslp_risk[6])

                frequencies_risk.append(item.elimination_risk[2])
                sums_damage_risk.append(item.elimination_risk[3])
                maths_expectation.append(item.elimination_risk[4])
                men_dead.append(item.elimination_risk[5])
                men_injured.append(item.elimination_risk[6])

            risk_table = [
                {'scenario_risk': scenario_risk, 'name_equp': name_equp, 'frequency_risk': frequency_risk, 'sum_damage_risk': sum_damage_risk,
                 'math_expectation': math_expectation, 'people_dead': people_dead, 'people_injured': people_injured}
                for
                scenario_risk, name_equp, frequency_risk, sum_damage_risk, math_expectation, people_dead, people_injured in
                zip(scenarios_risk, name_equps, frequencies_risk, sums_damage_risk, maths_expectation, men_dead, men_injured)]

            return risk_table

        def math_risk_part():
            # таблица результатов расчета риска
            scenarios_risk = ["C1_1", "C2_1", "C3_1", "C4_1"] * len(self.list_device)
            name_equps =[]
            frequencies_risk = []
            sums_damage_risk = []
            maths_expectation = []
            men_dead = []
            men_injured = []

            for item in self.list_device:
                name_equps.extend([item.name for _ in range(4)])
                frequencies_risk.append(item.explosion_risk_part[2])
                sums_damage_risk.append(item.explosion_risk_part[3])
                maths_expectation.append(item.explosion_risk_part[4])
                men_dead.append(item.explosion_risk_part[5])
                men_injured.append(item.explosion_risk_part[6])

                frequencies_risk.append(item.strait_risk_part[2])
                sums_damage_risk.append(item.strait_risk_part[3])
                maths_expectation.append(item.strait_risk_part[4])
                men_dead.append(item.strait_risk_part[5])
                men_injured.append(item.strait_risk_part[6])

                frequencies_risk.append(item.lslp_risk_part[2])
                sums_damage_risk.append(item.lslp_risk_part[3])
                maths_expectation.append(item.lslp_risk_part[4])
                men_dead.append(item.lslp_risk_part[5])
                men_injured.append(item.lslp_risk_part[6])

                frequencies_risk.append(item.elimination_risk_part[2])
                sums_damage_risk.append(item.elimination_risk_part[3])
                maths_expectation.append(item.elimination_risk_part[4])
                men_dead.append(item.elimination_risk_part[5])
                men_injured.append(item.elimination_risk_part[6])

            risk_table_part = [
                {'scenario_risk': scenario_risk, 'name_equp': name_equp, 'frequency_risk': frequency_risk, 'sum_damage_risk': sum_damage_risk,
                 'math_expectation': math_expectation, 'people_dead': people_dead, 'people_injured': people_injured}
                for
                scenario_risk, name_equp, frequency_risk, sum_damage_risk, math_expectation, people_dead, people_injured in
                zip(scenarios_risk, name_equps, frequencies_risk, sums_damage_risk, maths_expectation, men_dead, men_injured)]

            return risk_table_part


        if len(self.list_device) == 0:
            return
        path_template = Path(os.getcwd())
        doc = DocxTemplate(f'{path_template}\\templates\\temp_rpz.docx')
        equp_table = equipment()
        mass_sub_table = mass_in_equipment()
        mass_crash_table = mass_crash()
        mass_crash_table_part = mass_crash_part()
        most_dangerous = most_dangerous()
        most_possible = most_possible()
        C2_table_factor = explosion_crash()
        C2_table_factor_part = explosion_crash_part()
        C1_table_factor = fire_crash()
        C1_table_factor_part = fire_crash_part()
        C3_table_factor = lclp_crash()
        C3_table_factor_part = lclp_crash_part()
        damage_table = damage()
        damage_table_part = damage_part()
        risk_table = math_risk()
        risk_table_part = math_risk_part()


        context = {'company_name': self.name,
                   'project_name': self.project,
                   'project_shifr': self.number,
                   'tom_shifr': self.code,
                   'year': date.today().year,
                   'water_cut': self.list_device[-1].water_cut,
                   'sulfur': self.list_device[-1].sulfur,
                   'resins': self.list_device[-1].resins,
                   'asphalt': self.list_device[-1].asphalt,
                   'paraffin': self.list_device[-1].paraffin,
                   'density': self.list_device[-1].density,
                   'viscosity': self.list_device[-1].viscosity,
                   'hydrogen_sulfide ': self.list_device[-1].hydrogen_sulfide,
                   'density_gas': self.list_device[-1].density_gas,
                   'project_description': self.description,
                   'equp_table': equp_table,
                   'mass_sub_table': mass_sub_table,
                   'sum_sub': sum([round(i.mass_sub / 1000, 2) for i in self.list_device]),
                   'automation': self.automation,
                   'mass_crash_table': mass_crash_table,
                   'mass_crash_table_part': mass_crash_table_part,
                   'most_possible': most_possible,
                   'most_dangerous': most_dangerous,
                   'C2_table_factor': C2_table_factor,
                   'C2_table_factor_part': C2_table_factor_part,
                   'C1_table_factor': C1_table_factor,
                   'C1_table_factor_part': C1_table_factor_part,
                   'C3_table_factor': C3_table_factor,
                   'C3_table_factor_part': C3_table_factor_part,
                   'damage_table': damage_table,
                   'damage_table_part': damage_table_part,
                   'risk_table': risk_table,
                   'risk_table_part': risk_table_part,

                   }
        doc.render(context)
        path_save = os.environ['USERPROFILE']
        doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')


if __name__ == '__main__':
    # 1. Создадим новые объекты
    container_dict = {
        'name': 'Е-3',
        'name_full': 'Емкость',
        'located': 'УПСВН',
        'material': 'Ст3',
        'ground': 'Надземное',
        'target': 'Хранение нефти',
        'length': 0,  # км
        'diameter': 0,  # мм
        'pressure': 0.28,  # кПа
        'temperature': 30,  # град.С
        'volume': 100,  # м3
        'completion': 0.8,  # - (степень заполнения)
        'spreading': 20,  # м^-1
        'type': 1,  # тип оборудования
        'place': 0.1,  # коэф.участия во взрыве
        'death_person': 1,
        'injured_person': 2,
        'time_person': 0.33,
        'density': 750,  # кг/м3
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

    }

    tube_dict = {
        'name': 'Нефтепровод от К-12 до т.3.',
        'name_full': 'Нефтепровод',
        'located': 'Зимнее м.н.',
        'material': 'В20',
        'ground': 'Подземное',
        'target': 'Транспорт нефти',
        'length': 0.88,  # км
        'diameter': 114,  # мм
        'pressure': 0.38,  # кПа
        'temperature': 10,  # град.С
        'volume': 0,  # м3
        'completion': 1,  # - (степень заполнения)
        'spreading': 20,  # м^-1
        'type': 0,  # тип оборудования
        'place': 0.1,  # коэф.участия во взрыве
        'death_person': 1,
        'injured_person': 1,
        'time_person': 0.13,
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

    }

    test_container = Device(container_dict)
    test_tube = Device(tube_dict)
    # print(test_container.volume_sub)
    # print(test_container.mass_sub)
    # print(test_container.square_sub)
    # print(test_container.evaporated_sub)
    # print(test_container.probability)
    # print(test_container.scenarios_full)
    # print(test_container.explosion_radius)
    # print(test_container.fire_radius)
    # print(test_container.lclp_radius)
    # print(test_container.explosion_damage)
    # print(test_container.strait_damage)
    # print(test_container.lclp_damage)
    # print(test_container.elimination_damage)
    # print(test_container.explosion_risk)
    # print(test_container.strait_risk)
    # print(test_container.lslp_risk)
    # print(test_container.elimination_risk)
    # print(20 * '-')
    # print(20 * '-')
    # print(test_container.volume_sub_part)
    # print(test_container.mass_sub_part)
    # print(test_container.square_sub_part)
    # print(test_container.evaporated_sub_part)
    # print(test_container.probability_part)
    # print(test_container.scenarios_part)
    # print(test_container.explosion_radius_part)
    # print(test_container.fire_radius_part)
    # print(test_container.lclp_radius_part)
    # print(test_container.explosion_damage_part)
    # print(test_container.strait_damage_part)
    # print(test_container.lclp_damage_part)
    # print(test_container.elimination_damage_part)
    # print(test_container.explosion_risk_part)
    # print(test_container.strait_risk_part)
    # print(test_container.lslp_risk_part)
    # print(test_container.elimination_risk_part)
    # print(test_container.group_risk)
    # print(test_container.individual_risk)
    # 2. Создадим новый ОПО
    test_obj = Dangerous_object()
    test_obj.append_device(test_container)
    test_obj.append_device(test_tube)
    test_obj.create_rpz()
