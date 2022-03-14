import math
from typing import Any, Union
import os
from datetime import date
from docxtpl import DocxTemplate, InlineImage
from pathlib import Path
from docx.shared import Mm
import numbers

TIME_EVAPORATED = 3600  # 3600 секунд, время испарения


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
        self.steam_pressure = float(char_set["steam_pressure"])
        self.spreading = float(char_set["steam_pressure"])
        # Характеристики вещества
        self.density = float(char_set["density"])
        self.density_gas = float(char_set["steam_pressure"])
        self.water_cut = float(char_set["density_gas"])
        self.sulfur = float(char_set["sulfur"])
        self.resins = float(char_set["resins"])  # смолы
        self.asphalt = float(char_set["asphalt"])  # асфальтены
        self.paraffin = float(char_set["paraffin"])
        self.viscosity = float(char_set["viscosity"])
        self.hydrogen_sulfide = float(char_set["hydrogen_sulfide"])  # сероводород
        self.molecular_weight = float(char_set["molecular_weight"])
        self.steam_pressure = float(char_set["steam_pressure"])
        # Расчетные значения
        self.volume_sub = self.emergency_volume()  # аварийный объем
        self.mass_sub = self.volume_sub / self.density # аварийная масса выброса
        self.square_sub = self.volume_sub * self.spreading  # аварийная плащодь пролива
        self.evaporated_sub = self.intensity() * self.square_sub * TIME_EVAPORATED # количество испарившегося вещества

    def emergency_volume(self):
        """
        Функция определения аварийного объема для оборудования (максимального), м3
        :return volume - объем, м3
        """
        volume = 0
        if self.length == 0 and self.volume == 0:
            raise ValueError("Объем емкости и длина трубы не могут быть нулевыми!")
        if self.length != 0 and self.volume != 0:
            raise ValueError("Объем емкости и длина трубы не могут быть одновременно заполненными!")
        if self.length != 0 and self.volume != 0:
            raise ValueError("Объем емкости и длина трубы не могут быть одновременно заполненными!")
        # Если трубопровод, то есть длина не равно 0
        if self.length != 0:
            volume = math.pi * math.pow(self.diameter / 2000, 2) * (self.length * 1000)
        # Если емкость, то есть объем не равен 0
        if self.volume != 0:
            volume = self.volume * self.completion
        return volume

    def intensity(self):
        return math.pow(10, -6) * math.sqrt(self.molecular_weight) * self.steam_pressure


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

    # def device_char_table(self):
    #     """Функция создания таблицы с характеристиками опасных веществ"""
    #
    #     def create_str(i: int) -> str:
    #         """Подфункция формирования строки с характеристиками для таблицы"""
    #         char = ''
    #         if self.list_device[i].length != 0:
    #             char = char + "L = " + str(self.list_device[i].length) + " км\n"
    #         if self.list_device[i].diameter != 0:
    #             char = char + "D = " + str(self.list_device[i].diameter) + " мм\n"
    #         if self.list_device[i].pressure != 0:
    #             char = char + "P = " + str(self.list_device[i].pressure) + " МПа\n"
    #         if self.list_device[i].volume != 0:
    #             char = char + "V = " + str(self.list_device[i].volume) + " м3\n"
    #         if self.list_device[i].completion != 0:
    #             char = char + "a = " + str(self.list_device[i].completion) + " -\n"
    #         return char
    #
    #     pozitions = [self.list_device[i].name for i in range(0, len(self.list_device))]
    #     name_equps = [self.list_device[i].material for i in range(0, len(self.list_device))]
    #     locations = [self.list_device[i].ground for i in range(0, len(self.list_device))]
    #     numbers = ["1" for _ in range(0, len(self.list_device))]
    #     appointments = [self.list_device[i].target for i in range(0, len(self.list_device))]
    #     characteristics = [create_str(i) for i in range(0, len(self.list_device))]
    #     device_char = [{'pozition': pozition, 'name_equp': name_equp, 'location': location, 'number': number,
    #                     'appointment': appointment, 'characteristic': characteristic}
    #                    for pozition, name_equp, location, number, appointment, characteristic in
    #                    zip(pozitions, name_equps, locations, numbers, appointments, characteristics)]
    #
    #     return device_char
    #
    # def mass_sub_table(self):
    #     """Функция создания таблицы с распределением опасного вещества"""
    #
    #     def create_num(i: int) -> str:
    #         """Подфункция формирования строки  с количеством оборудования"""
    #         char = ''
    #         if self.list_device[i].length != 0:
    #             char = char + str(self.list_device[i].length) + " км"
    #         if self.list_device[i].volume != 0:
    #             char = "1"
    #         return char
    #
    #     def create_quantity(i: int) -> str:
    #         """Подфункция формирования строки  с количеством оборудования"""
    #         quantity = 0
    #         if self.list_device[i].length != 0:
    #             volume = math.pi * math.pow(self.list_device[i].diameter / 2000, 2) * (
    #                     self.list_device[i].length * 1000)
    #             quantity = volume * self.sub.density / 1000
    #         if self.list_device[i].volume != 0:
    #             quantity = self.list_device[i].volume * self.sub.density / 1000 * self.list_device[i].completion + \
    #                        self.list_device[i].volume * self.sub.density_gas / 1000 * (
    #                                1 - self.list_device[i].completion)
    #         # расчетные значения в класс
    #         self.list_device[i].volume_sub = quantity / (self.sub.density / 1000)
    #         self.list_device[i].square = self.list_device[i].volume_sub * SPREADING
    #         self.list_device[i].evaporated = math.pow(10,-6)*math.sqrt(self.sub.)*58
    #         return str(round(quantity, 1))
    #
    #     def create_phase(i: int) -> str:
    #         """Подфункция формирования строки  с количеством оборудования"""
    #         char = ''
    #         if self.list_device[i].length != 0:
    #             char = "ж.ф."
    #         if self.list_device[i].volume != 0:
    #             char = "ж.ф. + г.ф."
    #         return char
    #
    #     components = [self.list_device[i].located for i in range(0, len(self.list_device))]
    #     pozitions_with_sub = [str(self.list_device[i].name) + ', нефть' for i in range(0, len(self.list_device))]
    #     lenghts_or_num = [create_num(i) for i in range(0, len(self.list_device))]
    #     quantitis = [create_quantity(i) for i in range(0, len(self.list_device))]
    #     states = [create_phase(i) for i in range(0, len(self.list_device))]
    #     pressures = [self.list_device[i].pressure for i in range(0, len(self.list_device))]
    #     temperatures = [self.list_device[i].temperature for i in range(0, len(self.list_device))]
    #
    #     sub_table = [
    #         {'component': component, 'pozition_with_sub': pozition_with_sub, 'lenght_or_num': lenght_or_num,
    #          'quantity': quantity,
    #          'state': state, 'pressure': pressure, 'temperature': temperature}
    #         for component, pozition_with_sub, lenght_or_num, quantity, state, pressure, temperature in
    #         zip(components, pozitions_with_sub, lenghts_or_num, quantitis, states, pressures, temperatures)]
    #
    #     return sub_table, sum([float(i) for i in quantitis])
    #
    # def index_table(self):
    #     # индексы оборудования при обозначении сценария
    #     indexs = [i + 1 for i in range(0, len(self.list_device))]
    #     pozitions = [self.list_device[i].name for i in range(0, len(self.list_device))]
    #
    #     index_table = [{'pozition': pozition, 'index': index}
    #                    for pozition, index in
    #                    zip(pozitions, indexs)]
    #
    #     return index_table
    #
    # def mass_table(self):
    #     indexs = [i + 1 for i in range(0, len(self.list_device))]
    #     # TODO
    #     # TODO
    #     # TODO
    #     # TODO # TODO # TODO # TODO # TODO # TODO
    #     scenarios = []
    #     for i in indexs:
    #         scenarios += scenarios + [f"С1П{i}", f"С2П{i}", f"С3П{i}", f"С4П{i}"] + \
    #                      [f"С1ТР{i}", f"С2ТР{i}", f"С3ТР{i}", f"С4ТР{i}"] + \
    #                      [f"С1СВ{i}", f"С2СВ{i}", f"С3СВ{i}", f"С4СВ{i}"]
    #
    #     frequencis = []
    #     for i in indexs:
    #         frequencis += frequencis + [i if i == 'труба' else 3E-7 in data_for_table[10], f"С2П{i}", f"С3П{i}",
    #                                     f"С4П{i}"] + \
    #                       [f"С1ТР{i}", f"С2ТР{i}", f"С3ТР{i}", f"С4ТР{i}"] + \
    #                       [f"С1СВ{i}", f"С2СВ{i}", f"С3СВ{i}", f"С4СВ{i}"]
    #
    #     damaging_factors = ['Тепловое излучение',
    #                         'Ударная волна',
    #                         'Тепловое излучение',
    #                         'Воздействие поллютанта'] * len(scenarios)
    #
    #     effects = ['Термический ожог',
    #                'Поражение избыточным давлением',
    #                'Термический ожог',
    #                'Загрязнение окружающей среды'] * len(scenarios)
    #
    #     sub_mass_alls = [20,
    #                      30,
    #                      40,
    #                      50] * len(scenarios)
    #
    #     sub_mass_parts = [2,
    #                       3,
    #                       4,
    #                       5] * len(scenarios)
    #
    #     mass_table = [{'scenario': scenario, 'frequency': frequency, 'damaging_factor': damaging_factor,
    #                    'effect': effect, 'sub_mass_all': sub_mass_all, 'sub_mass_part': sub_mass_part}
    #                   for scenario, frequency, damaging_factor, effect, sub_mass_all, sub_mass_part in
    #                   zip(scenarios, frequencis, damaging_factors, effects, sub_mass_alls, sub_mass_parts)] * len(
    #         scenarios)


if __name__ == '__main__':
    # 1. Инициализируем вещество и объект
    sub = Substance()
    start_obj = Dangerous_object()
    # создадим оборудование
    dev1 = Device()
    # Добавим оборудование в список
    start_obj.append_device(dev1, sub)

    # path_template = Path(os.getcwd())
    # doc = DocxTemplate(f'{path_template}\\templates\\temp_rpz.docx')
    # заполнение шаблона
    # sub_table, quantitis = start_obj.mass_sub_table()
    # context = {'company_name': start_obj.name,
    #            'project_name': start_obj.project,
    #            'project_shifr': start_obj.number,
    #            'tom_shifr': start_obj.code,
    #            'year': date.today().year,
    #            'water_cut': start_obj.sub.water_cut,
    #            'sulfur': start_obj.sub.sulfur,
    #            'resins': start_obj.sub.resins,
    #            'asphalt': start_obj.sub.asphalt,
    #            'paraffin': start_obj.sub.paraffin,
    #            'density': start_obj.sub.density,
    #            'viscosity': start_obj.sub.viscosity,
    #            'hydrogen_sulfide ': start_obj.sub.hydrogen_sulfide,
    #            'density_gas': start_obj.sub.density_gas,
    #            'project_description': start_obj.description,
    #            'equp_table': start_obj.device_char_table(),
    #            'mass_sub_table': sub_table,
    #            'sum_sub': quantitis,
    #            'automation': start_obj.automation,
    #            'index_table': start_obj.index_table(),
    #            'mass_crash_table': mass_crash_table,
    #            'most_possible': "сценарий А12(27), А12(30) Трубопровод от скв.4722 до БГЗЖ загрязнение окружающей среды,",
    #            'most_dangerous': "сценарий А12(25), А12(26), А12(28), А12(29) Трубопровод от БГЗЖ К-1063 до т.9 - участок №1 пожар.",
    #            'C2_table_factor': C2_table_factor,
    #            'C1_table_factor': C1_table_factor,
    #            'C3_table_factor': C3_table_factor,
    #            'damage_table': damage_table,
    #            'risk_table': risk_table,
    #            'result_table': result_table,
    #            'fn': InlineImage(doc, f'{path_template}\\templates\\fn.jpg', width=Mm(160)),
    #            'fq': InlineImage(doc, f'{path_template}\\templates\\fq.jpg', width=Mm(160))
    #
    #            }
    #
    # doc.render(context)
    # path_save = os.environ['USERPROFILE']
    # doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')

# name = 'Трубопровод от скв.4763 до БГЗЖ'
#         located = "Тавельское м.н."
#         material = 'Трубопровод, сталь В20'
#         ground = 'Подземное'
#         target = 'Транспорт нефти'
#         length = 0.899
#         diameter = 114
#         pressure = 0.25
#         temperature = 10
#         volume = 0
#         completion = 0  # степень заполнения
#         steam_pressure = 35  # давление пара
#         # расчетные значения
#         volume_sub = 0
#         square = 0
#         evaporated = 0
