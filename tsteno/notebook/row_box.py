import re


class RowBox:
    def __init__(self, boxes):
        self.boxes = boxes

    def parse_box_el(self, el):
        return re.sub(r"\"<(.*)>\"", "\"\\1\"", el, 0, re.MULTILINE)

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
