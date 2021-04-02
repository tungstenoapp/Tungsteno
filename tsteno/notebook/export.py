import uuid

notebook_header = "(* Content-type: application/vnd.wolfram.mathematica *)"
notebook_bottom = "(* End of Notebook Content *)"


def export_nb(cells):
    notebook_content = notebook_header + "\n"

    notebook_content += "Notebook[{"

    cell_num = 1
    for cell in cells:
        notebook_content += "Cell[BoxData["
        notebook_content += "RowBox[{\"" + cell + "\"}]], "
        notebook_content += """"Input",
        CellLabel->"In[{}]:=",ExpressionUUID->"{}"]
        """.format(cell_num, uuid.uuid4())

        notebook_content += ","
        cell_num += 1

    if len(cells) > 0:
        notebook_content = notebook_content[:-1]
    notebook_content += "}, "

    notebook_content += """
    WindowSize -> {606., 658.5},
    WindowMargins -> {{Automatic, 342}, {1.5, Automatic}},
    FrontEndVersion -> "Tungsteno Open Source Alternative",
    StyleDefinitions -> "Default.nb"
    ]
    """

    notebook_content = notebook_content + "\n" + notebook_bottom

    return notebook_content
