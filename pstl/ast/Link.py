from pstl.ast.Node import Node
from pylatex import Figure
class AQ_Link(Node):
    def __init__(self, ctx, parent):
        super(AQ_Link, self).__init__(ctx, parent)


    def latex(self):
        return None