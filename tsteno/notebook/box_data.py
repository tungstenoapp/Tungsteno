class BoxData:
    def __init__(self, boxes):
        self.boxes = boxes

    def cli(self):
        return self.boxes.cli()
