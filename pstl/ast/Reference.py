from pstl.ast.Node import Node
from pylatex.base_classes.command import Command
class AQ_Reference(Node):
    def __init__(self, ctx, label, parent = None):
        self.label = label
        super(AQ_Reference, self).__init__(ctx, parent)


    def latex(self):
        _reference = Command("ref", self.label)
        return _reference
