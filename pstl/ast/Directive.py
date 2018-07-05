from pstl.ast.Node import Node
import logging
class AQ_Directive(Node):
    def __init__(self, ctx, name = 0, value = "", parent = None):
        super(AQ_Directive, self).__init__(ctx, parent)
        self.name = name
        self.value = value.strip()

    def getName(self):
        return self.name

    def __repr__(self):
        return f"<directive name='{self.name}' value='{self.value}'/>"

    def __str__(self):
        return f"<directive name='{self.name}' value='{self.value}'/>"
    def latex(self):
        return None