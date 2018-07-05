from pstl.ast.Node import Node
from pylatex.utils import NoEscape
class AQ_LatexFragment(Node):
    def __init__(self, ctx, content, parent = None):
        self.content = content
        super(AQ_LatexFragment, self).__init__(ctx, parent)


    def latex(self):
        return NoEscape('$'+ self.content + '$')
