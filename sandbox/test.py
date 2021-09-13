

class Table:
    def __init__(self, size):
        self.size = size

class Table2(Table):
    def __init__(self, size, color):
        Table.__init__(self, size)
        self.color = color

if __name__ == '__main__':
    cls = Table2(12,13)