import win32com.client
import xlwings as xw

class Excel:
    def __init__(self) -> None:
        self.app = xw.App(visible=True,add_book=True)
        self.wb = self.app.books.active
        self.sheet = self.wb.sheets[0]

    def create(self, columns: list) -> None:
        # Ширина первой колонки
             #
        # Создаем колонки
        for i in range(len(columns)):
            xw.Range((i + 1, 1)).value = columns[i]

    def write(self, columns: list) -> None:

               # ищем пустой столбец для записи в файле экселя
               i = 1
               while i < 10000:
                   # т.е. строка постоянно 1, а столбец мы ищем перебором
                   val = xw.Range((1, i)).value
                   if val == None:
                       break
                   i = i + 1
               # когда мы нашли пустой столбец
               # нам в цикле нужно его заполнить
               # данными из списка radius_CZA
               k = 1
               for rec in columns:
                   xw.Range((k, i)).value = rec
                   k = k + 1

    def close(self)-> None:
        self.wb.close()
        # Закроем объект
        self.app.quit()
