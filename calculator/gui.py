import os

from docxtpl import DocxTemplate
from pathlib import Path

path_template = Path(os.getcwd())
doc = DocxTemplate(f'{path_template}\\templates\\temp_rpz.docx')
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

           }

doc.render(context)
# doc.render(context2)
path_save = os.environ['USERPROFILE']
doc.save(f'{path_save}\\Desktop\\generated_rpz.docx')

if __name__ == '__main__':
    pass
