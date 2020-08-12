class Cell:
    def __init__(self, contents):
        print(contents)
        self.contents = contents

    def __repr__(self):
        return str(self.contents)


class CellGroupData:
    def __init__(self, cells):
        self.cells = cells

    def __repr__(self):
        return str(self.cells)
