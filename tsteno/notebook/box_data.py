class BoxData:
    def __init__(self, boxes):
        self.boxes = boxes

    def cli(self):
        return self.boxes.cli()

    def dump(self):
        return {
            'boxes': self.boxes.dump(),
            '__cls__': 'box_data'
        }
