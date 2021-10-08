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

           }

doc.render(context)
path_save = os.environ['USERPROFILE']
doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')

if __name__ == '__main__':
    pass
