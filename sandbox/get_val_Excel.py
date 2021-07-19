import win32com.client
Excel = win32com.client.Dispatch("Excel.Application")
print(Excel.ActiveWorkbook.Name)
print(Excel.ActiveSheet.Name)
sheet = Excel.ActiveSheet

# Excel.Selection.Value = "Hello World"
vals = Excel.Selection.Value
print(len(vals))

if __name__ == '__main__':
    pass