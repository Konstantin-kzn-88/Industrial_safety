import os
from datetime import date

from docxtpl import DocxTemplate, InlineImage
from pathlib import Path
from docx.shared import Mm

path_template = Path(os.getcwd())

doc = DocxTemplate(f'{path_template}\\templates\\temp_rpz.docx')

# Оборудование для расчета
data_for_text = ["ЗАО «Предприятие Кара Алтын»",
                 "Обустройствo куста скважин №1063 Тавельского нефтяного месторождения",
                 "55-20",
                 "12.1.2",
                 [20, 30, 40, 50, 60, 20, 20, 20, 10],
                 "Данной проектной документацией предусмотренно многое...",
                 "В разделе «Автоматизация» предусматривается решение вопросов автоматизации технологических "
                 "процессов и объектов в объеме основных положений по обустройству нефтяных промыслов",
                 ]

data_for_table = [['Трубопровод от скв.4763 до БГЗЖ',
                   'Трубопровод от скв.4762 до БГЗЖ',
                   'Трубопровод от скв.4722 до БГЗЖ',
                   'Емкость Е-1'],  # 0

                  ['Трубопровод, сталь В20',
                   'Трубопровод, сталь В20',
                   'Трубопровод, сталь В20',
                   'Трубопровод, сталь В20'],  # 1

                  ['Подземное',
                   'Подземное',
                   'Подземное',
                   'Надземное'],  # 2

                  ['Транспорт нефти',
                   'Транспорт нефти',
                   'Транспорт нефти',
                   'Хранение нефти'],  # 3

                  ['L = 0,029 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'L = 0,028 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'L = 0,027 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'V = 89 м3;\na = 0,8 -;\nP = 0,24 МПа'],  # 4

                  ['Тавельское м.н.',
                   'Тавельское м.н.',
                   'Тавельское м.н.',
                   'УПСВ'],  # 5

                  [0.27, 0.26, 0.25, 1],  # 6
                  [0.159, 0.158, 0.14, 65],  # 7
                  [0.25, 0.158, 0.14, 0.36],  # 8
                  [10, 10, 10, 25],  # 9
                  ["труба", "труба", "труба", "емкость"]  # 10

                  ]

# Оборудование
pozitions = data_for_table[0]

name_equps = data_for_table[1]

locations = data_for_table[2]

numbers = ["1" for _ in range(0, len(pozitions))]

appointments = data_for_table[3]

characteristics = data_for_table[4]

equp_table = [{'pozition': pozition, 'name_equp': name_equp, 'location': location, 'number': number,
               'appointment': appointment, 'characteristic': characteristic}
              for pozition, name_equp, location, number, appointment, characteristic in
              zip(pozitions, name_equps, locations, numbers, appointments, characteristics)]

# Распредление опасного вещества
components = data_for_table[5]

pozitions_with_sub = [i + ', нефть' for i in data_for_table[0]]

lenghts_or_num = [(str(i) + " км") if i != 1 else 1 for i in data_for_table[6]]

quantitis = data_for_table[7]

states = ['Ж.ф.' if i != 1 else 'Ж.ф.+п.г.ф.' for i in data_for_table[6]]

pressures = data_for_table[8]

temperatures = data_for_table[9]

mass_sub_table = [{'component': component, 'pozition_with_sub': pozition_with_sub, 'lenght_or_num': lenght_or_num,
                   'quantity': quantity,
                   'state': state, 'pressure': pressure, 'temperature': temperature}
                  for component, pozition_with_sub, lenght_or_num, quantity, state, pressure, temperature in
                  zip(components, pozitions_with_sub, lenghts_or_num, quantitis, states, pressures, temperatures)]

# индексы оборудования при обозначении сценария
indexs = [i + 1 for i in range(0, len(pozitions))]

index_table = [{'pozition': pozition, 'index': index}
               for pozition, index in
               zip(pozitions, indexs)]

# массы вещества участвующего в аварии
scenarios = []
for i in indexs:
    scenarios += scenarios + [f"С1П{i}", f"С2П{i}", f"С3П{i}", f"С4П{i}"] + \
                 [f"С1ТР{i}", f"С2ТР{i}", f"С3ТР{i}", f"С4ТР{i}"] + \
                 [f"С1СВ{i}", f"С2СВ{i}", f"С3СВ{i}", f"С4СВ{i}"]

frequencis = []
for i in indexs:
    frequencis += frequencis + [i if i == 'труба' else 3E-7 in data_for_table[10], f"С2П{i}", f"С3П{i}", f"С4П{i}"] + \
                 [f"С1ТР{i}", f"С2ТР{i}", f"С3ТР{i}", f"С4ТР{i}"] + \
                 [f"С1СВ{i}", f"С2СВ{i}", f"С3СВ{i}", f"С4СВ{i}"]

damaging_factors = ['Тепловое излучение',
                    'Ударная волна',
                    'Тепловое излучение',
                    'Воздействие поллютанта'] * len(scenarios)

effects = ['Термический ожог',
           'Поражение избыточным давлением',
           'Термический ожог',
           'Загрязнение окружающей среды'] * len(scenarios)

sub_mass_alls = [20,
                 30,
                 40,
                 50]* len(scenarios)

sub_mass_parts = [2,
                  3,
                  4,
                  5]* len(scenarios)

mass_crash_table = [{'scenario': scenario, 'frequency': frequency, 'damaging_factor': damaging_factor,
                     'effect': effect, 'sub_mass_all': sub_mass_all, 'sub_mass_part': sub_mass_part}
                    for scenario, frequency, damaging_factor, effect, sub_mass_all, sub_mass_part in
                    zip(scenarios, frequencis, damaging_factors, effects, sub_mass_alls, sub_mass_parts)]* len(scenarios)

# таблица взрывов
scenarios_C2 = ['C2П1',
                'C2П2',
                'C2П3',
                'C2П4']

sub_masses_C2 = [10,
                 20,
                 30,
                 40]

heats_C2 = [46000,
            47000,
            47500,
            48800]

velocitis_C2 = [150,
                160,
                170,
                180]

pressures_100 = [120,
                 10,
                 50,
                 325]

pressures_53 = [150,
                20,
                100,
                453]

pressures_28 = [180,
                30,
                200,
                589]

pressures_12 = [200,
                40,
                250,
                698]

pressures_5 = [250,
               50,
               300,
               4123]

pressures_3 = [300,
               60,
               698,
               10258]

men_C2 = ["1/3",
          "1/6",
          "1/2",
          "1/1"]

C2_table_factor = [{'scenario_C2': scenario_C2, 'sub_mass_C2': sub_mass_C2, 'heat_C2': heat_C2,
                    'velocity_C2': velocity_C2, 'dp_100': dp_100, 'dp_53': dp_53, 'dp_28': dp_28,
                    'dp_12': dp_12, 'dp_5': dp_5, 'dp_3': dp_3, 'people_C2': people_C2}
                   for
                   scenario_C2, sub_mass_C2, heat_C2, velocity_C2, dp_100, dp_53, dp_28, dp_12, dp_5, dp_3, people_C2 in
                   zip(scenarios_C2, sub_masses_C2, heats_C2, velocitis_C2, pressures_100, pressures_53, pressures_28,
                       pressures_12, pressures_5, pressures_3, men_C2)]

# таблица пожаров
scenarios_C1 = ['C1П1',
                'C1П2',
                'C1П3',
                'C1П4']

squares_C1 = [10,
              20,
              30,
              40]

heats_C1 = [25,
            26,
            27,
            28]

burnouts_C1 = [0.06,
               0.06,
               0.06,
               0.06]

intensitis_17 = [120,
                 10,
                 50,
                 325]

intensitis_12 = [150,
                 20,
                 100,
                 453]

intensitis_10 = [180,
                 30,
                 200,
                 589]

intensitis_7 = [200,
                40,
                250,
                698]

intensitis_4 = [250,
                50,
                300,
                4123]

intensitis_1 = [300,
                60,
                698,
                10258]

men_C1 = ["1/3",
          "1/6",
          "1/2",
          "1/1"]

C1_table_factor = [{'scenario_C1': scenario_C1, 'square_C1': square_C1, 'heat_C1': heat_C1,
                    'burnout_C1': burnout_C1, 'q_17': q_17, 'q_12': q_12, 'q_10': q_10,
                    'q_7': q_7, 'q_4': q_4, 'q_1': q_1, 'people_C1': people_C1}
                   for
                   scenario_C1, square_C1, heat_C1, burnout_C1, q_17, q_12, q_10, q_7, q_4, q_1, people_C1 in
                   zip(scenarios_C2, squares_C1, heats_C2, burnouts_C1, intensitis_17, intensitis_12, intensitis_10,
                       intensitis_7, intensitis_4, intensitis_1, men_C1)]

# таблица вспышек
scenarios_C3 = ['C3П1',
                'C3П2',
                'C3П3',
                'C3П4']

sub_masses_C3 = [10,
                 20,
                 30,
                 40]

heats_C3 = [46000,
            47000,
            47500,
            48800]

radiuses_nkpr_C3 = [150,
                    160,
                    170,
                    180]

radiuses_vsp_C3 = [120,
                   10,
                   50,
                   325]

men_C3 = ["1/3",
          "1/6",
          "1/2",
          "1/1"]

C3_table_factor = [{'scenario_C3': scenario_C3, 'sub_mass_C3': sub_mass_C3, 'heat_C3': heat_C3,
                    'radius_nkpr_C3': radius_nkpr_C3, 'radius_vsp_C3': radius_vsp_C3, 'people_C3': people_C3}
                   for
                   scenario_C3, sub_mass_C3, heat_C3, radius_nkpr_C3, radius_vsp_C3, people_C3 in
                   zip(scenarios_C3, sub_masses_C3, heats_C3, radiuses_nkpr_C3, radiuses_vsp_C3, men_C3)]

# таблица ущерба
scenarios_damage = ['C3П1',
                    'C3П2',
                    'C3П3',
                    'C3П4']

straights = [10,
             20,
             30,
             40]

localizations = [46000,
                 47000,
                 47500,
                 48800]

economics = [150,
             160,
             170,
             180]

works = [120,
         10,
         50,
         325]

indirects = [120,
             10,
             50,
             325]

ecologys = [120,
            10,
            50,
            325]

sums_damage = [120,
               10,
               50,
               325]

damage_table = [{'scenario_damage': scenario_damage, 'straight': straight, 'localization': localization,
                 'economic': economic, 'work': work, 'indirect': indirect, 'ecology': ecology, 'sum_damage': sum_damage}
                for
                scenario_damage, straight, localization, economic, work, indirect, ecology, sum_damage in
                zip(scenarios_damage, straights, localizations, economics, works, indirects, ecologys, sums_damage)]

# таблица результатов расчета риска
scenarios_risk = ['C3П1',
                  'C3П2',
                  'C3П3',
                  'C3П4']

frequencies_risk = ['5e-3',
                    '3e-3',
                    '6e-3',
                    '1e-3']

sums_damage_risk = [120,
                    10,
                    50,
                    325]

maths_expectation = [120,
                     10,
                     50,
                     325]

men_dead = ["1/3",
            "1/6",
            "1/2",
            "1/1"]

men_injured = ["1/3",
               "1/6",
               "1/2",
               "1/1"]

risk_table = [{'scenario_risk': scenario_risk, 'frequency_risk': frequency_risk, 'sum_damage_risk': sum_damage_risk,
               'math_expectation': math_expectation, 'people_dead': people_dead, 'people_injured': people_injured}
              for
              scenario_risk, frequency_risk, sum_damage_risk, math_expectation, people_dead, people_injured in
              zip(scenarios_risk, frequencies_risk, sums_damage_risk, maths_expectation, men_dead, men_injured)]

# таблица инд. и коллективного риска
pozitions_res = ['Трубопровод от скв.4763 до БГЗЖ',
                 'Трубопровод от скв.4762 до БГЗЖ',
                 'Трубопровод от скв.4722 до БГЗЖ',
                 'Трубопровод от БГЗЖ К-1063 до т.9']

maths_ind = ['5e-3',
             '3e-3',
             '6e-3',
             '1e-3']

maths_koll = ['5e-3',
              '3e-3',
              '6e-3',
              '1e-3']

result_table = [{'pozition_res': pozition_res, 'math_ind': math_ind, 'math_koll': math_koll, }
                for pozition_res, math_ind, math_koll in
                zip(pozitions_res, maths_ind, maths_koll)]

# заполнение шаблона
context = {'company_name': data_for_text[0],
           'project_name': data_for_text[1],
           'project_shifr': data_for_text[2],
           'tom_shifr': data_for_text[3],
           'year': date.today().year,
           'water_cut': data_for_text[4][0],
           'sulfur': data_for_text[4][1],
           'resins': data_for_text[4][2],
           'asphalt': data_for_text[4][3],
           'paraffin': data_for_text[4][4],
           'density': data_for_text[4][5],
           'viscosity': data_for_text[4][6],
           'hydrogen_sulfide ': data_for_text[4][7],
           'density_gas': data_for_text[4][8],
           'project_description': data_for_text[5],
           'equp_table': equp_table,
           'mass_sub_table': mass_sub_table,
           'sum_sub': sum(quantitis),
           'automation': data_for_text[6],
           'index_table': index_table,
           'mass_crash_table': mass_crash_table,
           'most_possible': "сценарий А12(27), А12(30) Трубопровод от скв.4722 до БГЗЖ загрязнение окружающей среды,",
           'most_dangerous': "сценарий А12(25), А12(26), А12(28), А12(29) Трубопровод от БГЗЖ К-1063 до т.9 - участок №1 пожар.",
           'C2_table_factor': C2_table_factor,
           'C1_table_factor': C1_table_factor,
           'C3_table_factor': C3_table_factor,
           'damage_table': damage_table,
           'risk_table': risk_table,
           'result_table': result_table,
           'fn': InlineImage(doc, f'{path_template}\\templates\\fn.jpg', width=Mm(160)),
           'fq': InlineImage(doc, f'{path_template}\\templates\\fq.jpg', width=Mm(160))

           }

doc.render(context)
path_save = os.environ['USERPROFILE']
doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')

if __name__ == '__main__':
    pass
