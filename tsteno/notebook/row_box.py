import re


class RowBox:
    def __init__(self, tmp):
        boxes = []

        for i in tmp:
            if isinstance(i, str):
                boxes.append(i)
            else:
                els = i.boxes
                boxes.extend(els)

        self.boxes = boxes

    def parse_box_el(self, el):
        if isinstance(el, str):
            return re.sub(r"\"<(.*)>\"", "\"\\1\"", el, 0, re.MULTILINE)
        return el

    def cli(self):
        box_elements = []

        for el in self.boxes:
            box_elements.append(self.parse_box_el(el))

        return box_elements

    def dump(self):
        box_elements = []

        for el in self.boxes:
            box_elements.append(self.parse_box_el(el))

        return {
            'boxes': box_elements,
            '__cls__': 'row_box'
        }
