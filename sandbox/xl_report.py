import win32com.client

class Excel:
    def __init__(self):
        self.Excel = win32com.client.Dispatch("Excel.Application")
        self.wb = self.Excel.Workbooks.Add()
        self.Excel.Visible = 1
        self.sheet = self.wb.ActiveSheet

    def create(self, columns: list):
        # Ширина первой колонки
        self.sheet.Range("A1").ColumnWidth = 50
        # Создаем колонки
        self.columns = columns
        for i in range(len(self.columns)):
            self.sheet.Cells(i+1, 1).value = self.columns[i]

    def close(self):
        self.wb.Close(SaveChanges=False)
        # Закроем COM объект
        self.Excel.Quit()