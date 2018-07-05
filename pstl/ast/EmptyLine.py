from pstl.ast.Node import Node
class AQ_EmptyLine(Node):
    def __init__(self, ctx, indentation = 0, level = 0, title = "", parent = None):
        super(AQ_EmptyLine, self).__init__(ctx, parent)


    def latex(self):
        from pylatex import LineBreak
        return LineBreak()

    def __repr__(self):
        return f"<linebreak/>"

    def __str__(self):
        return f"<linebreak/>"
