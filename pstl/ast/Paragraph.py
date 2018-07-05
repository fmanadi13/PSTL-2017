from pstl.ast.Node import Node
from pylatex.base_classes.command import Command
from pylatex.section import Paragraph, Section
from pylatex import TextBlock
from pylatex.utils import NoEscape, italic, bold, verbatim
class AQ_Paragraph(Node):

    def __init__(self, ctx, parent = None):
        super(AQ_Paragraph, self).__init__(ctx, parent)

    def latex(self):
        
       # _paragraph = Paragraph("", label = False)
        _paragraph = NoEscape()
        for line in self.children:
            _text_content = ""
            for i, span in enumerate(line.children):
                if span:
                    if isinstance(span, AQ_Text):
                        _text_content += span.latex()
                        if i == len(line.children) -1:
                            _paragraph += _text_content
                            _text_content = ""
                    else:
                        if _text_content != "":
                            _paragraph += _text_content
                            _text_content = ""
                        if isinstance(span.latex(), (NoEscape, str)):
                            _paragraph += span.latex()
                        else:
                            _paragraph += span.latex().dumps()
            _paragraph +='\n\n'

        return NoEscape(_paragraph)


class AQ_Line(Node):
    def __init__(self, ctx, parent = None):
        super(AQ_Line, self).__init__(ctx, parent)


    def latex(self):
        return None

class AQ_Span(Node):
    def __init__(self, ctx, parent = None):
        super(AQ_Span, self).__init__(ctx, parent)


    def latex(self):
        return None

class AQ_LatexEntity(Node):
    def __init__(self, ctx, name, parent = None):
        self.name = name
        super(AQ_LatexEntity, self).__init__(ctx, parent)


    def latex(self):
        return Command(self.name, '')

class AQ_Text(Node):
    def __init__(self, ctx, content, parent = None):
        self.content = content
        super(AQ_Text, self).__init__(ctx, parent)


    def latex(self):
        return self.content

class AQ_Emphasis(Node):
    def __init__(self, ctx, delimiter, parent = None):
        self.delimiter = delimiter
        super(AQ_Emphasis, self).__init__(ctx, parent)


    def latex(self):
        _content = ""
        for c in self.children:
            _content += c.latex()
        if self.delimiter == '/':
            return italic(_content, escape = False)
        elif self.delimiter == '*':
            return bold(_content, escape = False)