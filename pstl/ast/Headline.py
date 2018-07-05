from pstl.ast.Node import Node
from pylatex import Command
    
from pylatex.utils import NoEscape, bold

class AQ_Headline(Node):
    def __init__(self, ctx, indentation = 0, level = 1, title = "", parent = None):
        super(AQ_Headline, self).__init__(ctx, parent)
        self.indentation = indentation
        self.level = level
        self.title = title
        self.isQuestion = True

    def latex(self):
        #from pylatex import Section, Subsection, Subsubsection
        #if self.level == 1:
        #    return Section(self.title)
        #elif self.level == 2:
        #    return Subsection(self.title)
        #elif self.level == 3:
        #    return Subsubsection(self.title)
        return Command('question', bold( NoEscape( self.title) ) )
    def __repr__(self):
        return f"<headline level='{self.level}'>{self.title}</headline>"
    def __str__(self):
        return f"<headline level='{self.level}'>{self.title}</headline>"