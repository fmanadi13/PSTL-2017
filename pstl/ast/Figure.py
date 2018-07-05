from pstl.ast.Node import Node
from pylatex import Figure, SubFigure, StandAloneGraphic
from pylatex.utils import NoEscape
class AQ_Figure(Node):
    def __init__(self, ctx, uri, parent = None):
        self.uri = uri
        self.caption = ""
        self.name = ""
        self.attr_latex = ""
        self.attrs =dict()
        super(AQ_Figure, self).__init__(ctx, parent)
     
    def _parse_attr_latex(self):
        if self.attr_latex.strip() != "":
            _params = list(filter(lambda x: x != "", self.attr_latex.split(':')))
            for _param in _params:
                (key, value) = tuple(_param.split(' '))
                self.attrs[key] = value



    def latex(self):
        width = "auto"
        height = "auto"
        self._parse_attr_latex()
        if 'width' in self.attrs:
            width = self.attrs['width']
        if 'height' in self.attrs:
            width = self.attrs['height']
        _figure = Figure(position = 'h')
        _figure.add_image(self.uri, width = NoEscape(width), placement= NoEscape('\centering'))
        _figure.add_caption(self.caption)
        return _figure
