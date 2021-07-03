import win32com.client


class Excel:
    def __init__(self) -> None:
        self.Excel = win32com.client.Dispatch("Excel.Application")
        self.wb = self.Excel.Workbooks.Add()
        self.Excel.Visible = 1
        self.sheet = self.wb.ActiveSheet

    def create(self, columns: list) -> None:
        # Ширина первой колонки
        self.sheet.Range("A1").ColumnWidth = 50
        # Создаем колонки
        for i in range(len(columns)):
            self.sheet.Cells(i + 1, 1).value = columns[i]

    def write(self, columns: list) -> None:

               # ищем пустой столбец для записи в файле экселя
               i = 1
               while i < 10000:
                   # т.е. строка постоянно 1, а столбец мы ищем перебором
                   val = self.sheet.Cells(1, i).value
                   if val == None:
                       break
                   i = i + 1
               # когда мы нашли пустой столбец
               # нам в цикле нужно его заполнить
               # данными из списка radius_CZA
               k = 1
               for rec in columns:
                   self.sheet.Cells(k, i).value = rec
                   k = k + 1

    def close(self):
        self.wb.Close(SaveChanges=False)
        # Закроем COM объект
        self.Excel.Quit()
