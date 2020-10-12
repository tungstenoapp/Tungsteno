from .box_data import BoxData


class Cell:
    def __init__(self, cell_content, status, cell_properties):
        self.status = status
        self.cell_content = cell_content
        self.cell_properties = cell_properties

    def cli(self):
        if isinstance(self.cell_content, CellGroupData):
            return self.cell_content.cli()
        elif isinstance(self.cell_content, BoxData):
            if self.status == 'Input':
                return self.cell_content.cli()
        else:
            print(self.cell_content)
            raise Exception("Unable to construct cell object")

    def dump(self):
        if isinstance(self.cell_content, CellGroupData) or (
            isinstance(self.cell_content, BoxData) and self.status == 'Input'
        ):
            return {
                'content': self.cell_content.dump(),
                'status': self.status,
                'properties': self.cell_properties,
                '__cls__': 'cell'
            }


class CellGroupData:

    def __init__(self, cells, status):
        self.cells = cells
        self.status = status

    def cli(self):
        cell_result = []

        for cell in self.cells:
            one_cell_result = cell.cli()

            if isinstance(one_cell_result, list):
                cell_result = cell_result + one_cell_result
            elif one_cell_result is not None:
                cell_result.append(one_cell_result)

        return cell_result

    def dump(self):
        cell_dump = []

        for cell in self.cells:
            one_cell_dump = cell.dump()

            if one_cell_dump is not None:
                cell_dump.append(one_cell_dump)

        return {
            'cells': cell_dump,
            'status': self.status,
            '__cls__': 'cell_group_data'
        }
