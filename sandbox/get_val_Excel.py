import win32com.client
Excel = win32com.client.Dispatch("Excel.Application")
print(Excel.ActiveWorkbook.Name)
print(Excel.ActiveSheet.Name)
print(Excel.ActiveSheet.Select)
sheet = Excel.ActiveSheet

vals = [r[0].value for r in sheet.Range("A1:A2")]
print(vals)

if __name__ == '__main__':
    pass