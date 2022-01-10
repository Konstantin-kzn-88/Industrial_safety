import os

from docxtpl import DocxTemplate
from pathlib import Path

path_template = Path(os.getcwd())

doc = DocxTemplate(f'{path_template}\\templates\\temp_rpz.docx')

# Оборудование
pozitions = ['Трубопровод от скв.4763 до БГЗЖ',
             'Трубопровод от скв.4762 до БГЗЖ',
             'Трубопровод от скв.4722 до БГЗЖ',
             'Трубопровод от БГЗЖ К-1063 до т.9']

name_equps = ['Трубопровод, сталь В20',
              'Трубопровод, сталь В20',
              'Трубопровод, сталь В20',
              'Трубопровод, сталь В20']

locations = ['Подземное',
             'Подземное',
             'Подземное',
             'Подземное']

numbers = ['1',
           '1',
           '1',
           '1']

appointments = ['Транспорт нефти',
                'Транспорт нефти',
                'Транспорт нефти',
                'Транспорт нефти']

characteristics = ['L = 0,029 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'L = 0,028 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'L = 0,027 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа',
                   'L = 0,026 км;\nDвн = 89 мм;\nPн = 0,24 МПа;\nPк = 0,24 МПа']

equp_table = [{'pozition': pozition, 'name_equp': name_equp, 'location': location, 'number': number,
               'appointment': appointment, 'characteristic': characteristic}
              for pozition, name_equp, location, number, appointment, characteristic in
              zip(pozitions, name_equps, locations, numbers, appointments, characteristics)]

# Распредление опасного вещества
components = ['Тавельское м.н.',
              'Тавельское м.н.',
              'Тавельское м.н.',
              'Тавельское м.н.']
pozitions_with_sub = ['Трубопровод от скв.4763 до БГЗЖ, нефть',
                      'Трубопровод от скв.4762 до БГЗЖ, нефть',
                      'Трубопровод от скв.4722 до БГЗЖ, нефть',
                      'Трубопровод от БГЗЖ К-1063 до т.9, нефть']

lenghts_or_num = ['0.27 км',
                  '0.26 км',
                  '0.25 км',
                  '0.24 км']

quantitis = [0.159,
             0.158,
             0.14,
             0.13]

states = ['Ж.ф.+п.г.ф.',
          'Ж.ф.+п.г.ф.',
          'Ж.ф.+п.г.ф.',
          'Ж.ф.+п.г.ф.']

pressures = ['0,25',
             '0,26',
             '0,29',
             '1,31']

temperatures = ['10',
                '11',
                '12',
                '15']

mass_sub_table = [{'component': component, 'pozition_with_sub': pozition_with_sub, 'lenght_or_num': lenght_or_num,
                   'quantity': quantity,
                   'state': state, 'pressure': pressure, 'temperature': temperature}
                  for component, pozition_with_sub, lenght_or_num, quantity, state, pressure, temperature in
                  zip(components, pozitions_with_sub, lenghts_or_num, quantitis, states, pressures, temperatures)]

# индексы оборудования при обозначении сценария
indexs = ['1',
          '2',
          '3',
          '4']

index_table = [{'pozition': pozition, 'index': index}
               for pozition, index in
               zip(pozitions, indexs)]

# массы вещества участвующего в аварии
scenarios = ['C1П1',
             'C2П1',
             'C3П1',
             'C4П1']

frequencis = ['5e-3',
              '3e-3',
              '6e-3',
              '1e-3']

damaging_factors = ['Тепловое излучение',
                    'Ударная волна',
                    'Тепловое излучение',
                    'Воздействие поллютанта']

effects = ['Термический ожог',
           'Поражение избыточным давлением',
           'Термический ожог',
           'Загрязнение окружающей среды']

sub_mass_alls = [20,
                 30,
                 40,
                 50]

sub_mass_parts = [2,
                  3,
                  4,
                  5]

mass_crash_table = [{'scenario': scenario, 'frequency': frequency, 'damaging_factor': damaging_factor,
                     'effect': effect, 'sub_mass_all': sub_mass_all, 'sub_mass_part': sub_mass_part}
                    for scenario, frequency, damaging_factor, effect, sub_mass_all, sub_mass_part in
                    zip(scenarios, frequencis, damaging_factors, effects, sub_mass_alls, sub_mass_parts)]

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

# заполнение шаблона
context = {'company_name': "ЗАО «Предприятие Кара Алтын»",
           'project_name': "Обустройствo куста скважин №1063 Тавельского нефтяного месторождения",
           'project_shifr': "55-20",
           'tom_shifr': "12.1.2",
           'year': "2021",
           'water_cut': 20,
           'sulfur': 32,
           'resins': 22,
           'asphalt': 12,
           'paraffin': 52,
           'density': 850,
           'viscosity': 33,
           'hydrogen_sulfide ': "0,05",
           'density_gas': "1,25",
           'project_description': "Данной проектной документацией предусмотренно многое...",
           'equp_table': equp_table,
           'mass_sub_table': mass_sub_table,
           'sum_sub': sum(quantitis),
           'automation': "В разделе «Автоматизация» предусматривается решение вопросов автоматизации технологических "
                         "процессов и объектов в объеме основных положений по обустройству нефтяных промыслов",
           'index_table': index_table,
           'mass_crash_table': mass_crash_table,
           'most_possible': "сценарий А12(27), А12(30) Трубопровод от скв.4722 до БГЗЖ загрязнение окружающей среды,",
           'most_dangerous': "сценарий А12(25), А12(26), А12(28), А12(29) Трубопровод от БГЗЖ К-1063 до т.9 - участок №1 пожар.",
           'C2_table_factor': C2_table_factor,
           'C1_table_factor': C1_table_factor,
           'C3_table_factor': C3_table_factor,

           }

doc.render(context)
path_save = os.environ['USERPROFILE']
doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')

if __name__ == '__main__':
    pass
