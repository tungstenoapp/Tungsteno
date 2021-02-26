class Cell:
    def __init__(self, cell_id, content=None, status='Input', properties={}):
        self.cell_id = cell_id
        self.content = content
        self.status = status
        self.properties = properties

    def toDict(self):
        return {
            'id': self.cell_id,
            'content': '',
            'status': self.status,
            'properties': self.properties
        }
