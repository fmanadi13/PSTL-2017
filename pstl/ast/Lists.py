from pstl.ast.Node import Node
from pstl.ast.pylatex_extend.checkboxes import *
from pylatex.utils import NoEscape

class AQ_List(Node):
    def __init__(self, ctx, parent = None):
        self.items = []
        super(AQ_List, self).__init__(ctx, parent)

    def append(self, item):
        self.items.append(item)

class AQ_Itemize(Node):
    def __init__(self, ctx):
        super(AQ_ListItem, self).__init__(ctx)

    def appendItem(self, item):
        self.items.append(item)

    def latex(self):
        return None

class AQ_Enumerate (AQ_List):

    def __init__(self, ctx, parent = None):
        self.items = []
        pass

class AQ_Checkboxes(AQ_List):
    def __init__(self, ctx, parent = None):
        super(AQ_Checkboxes, self).__init__(ctx, parent)

    def latex(self):
        __list = Checkboxes()
        for i in self.items:
            __list.add_item(i.isChecked, NoEscape(i.latex()))

        return __list


class AQ_Item(Node):
    def __init__(self, ctx, isChecked = False, parent = None):
        self.isCheckbox = True
        self.isChecked = isChecked
        super(AQ_Item, self).__init__(ctx, parent)

    def latex(self):
        _content = ""
        _content = ''.join([child.latex() for child in self.children])


        return _content