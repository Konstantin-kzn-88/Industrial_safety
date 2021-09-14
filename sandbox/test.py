

class GUI:
    def __init__(self):
        self.qcombobox_state = "company"

class Table2(GUI):
    def __init__(self, color):
        GUI.__init__(self)
        self.color = color

if __name__ == '__main__':
    cls = Table2(12)