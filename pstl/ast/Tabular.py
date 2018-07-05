from pstl.ast.Node import Node
from pylatex import Tabular
class AQ_Tabular(Node):
    def __init__(self, ctx, parent = None):
        self.caption = ""
        self.name = ""
        self.attr_latex = ""
        super(AQ_Tabular, self).__init__(ctx, parent)
        


    def __maxColumns(self):
        max = 0
        for c in self.children:
            if len(c.children) > max:
                max = len(c.children)

        return max

    
    def appendChild(self, child):
        super().appendChild(child)
        self.updateColspans(child)

    def updateColspans(self, row):
        if len(self.children) < 1:
            return None
        colsWidth = []
        for c in self.children[0].children:
            colsWidth.append(c.width)
        currentWidth = colsWidth[0]
        i = 0
        if not row.isFullWidthHline():
            for c in row.children:
                colspan = 1
                if c.width == currentWidth:
                    c.colspan = colspan
                    i +=1
                    if(i<len(colsWidth)):
                        currentWidth = colsWidth[i]
                else:

                    while not c.width == currentWidth and not (c.width == (currentWidth -1)) and i+1 < len(colsWidth):
                        i = i+1
                        colspan += 1
                        currentWidth = currentWidth + (colsWidth[i] +1)


                    if i+1 < len(colsWidth):
                        i +=1
                        currentWidth = colsWidth[i]
                    c.colspan = colspan

    def latex(self):
        from pylatex import Document, Section, Subsection, Tabular, MultiColumn,\
                            MultiRow

        width = '|'
        for i in range(0, self.__maxColumns()):
            width += 'c|'
        t = Tabular(width)
        
        colsWidth = []
        for c in self.children[0].children:
            colsWidth.append(c.width)
        for r in self.children:
            if r.hasHline:
                if r.isFullWidthHline():
                    t.add_hline()
                else:
                    start = 1
                    cellsCount = 0
                    end = 0
                    hline = False
                    lastCell = None
                    for i, c in enumerate(r.children):
                        if c.isHline:
                            if start == 1:
                                start = r.children.index(c) + 1
                            cellsCount += c.colspan
                            if i == len(r.children) -1:
                                end = start + cellsCount -1
                                t.add_hline(start=start, end= end)
                        else:
                            end = start + cellsCount -1
                            if(start > 0 and end >= start):
                                t.add_hline(start=start, end= end)
                                start = end + 1
                            else:
                                start = start + c.colspan
                            cellsCount = 0
                            end = 0
            else:
                cellsObjects = r.children
                cells =  []
                
                i = 0
                for c in cellsObjects:
                    if c.colspan == 1:
                        cells.append(str(c.content))
                    else:
                        cells.append(MultiColumn(c.colspan, align='|c|', data= str(c.content)))

                
                t.add_row(cells)
        return t
        

    def __repr__(self):
        return f"<tabular max-cols='{self.__maxColumns()}'>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</tabular>"

    def __str__(self):
        return "<tabular>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</tabular>"

class AQ_TabularRow(Node):
    hasHline = False
    
    def __init__(self, ctx, parent = None):
        super(AQ_TabularRow, self).__init__(ctx, parent)

    def isFullWidthHline(self):
        if not self.hasHline:
            return False
        else:
            for c in self.children:
                if c.content == "":
                    return False
        return True


    def __repr__(self):
        return "<row>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</row>"

    def __str__(self):
        return "<row>\n"+ ('\n'.join([c.__repr__() for c in self.children])) +"\n</row>"

class AQ_TabularCell(Node):

    def __init__(self, ctx, content = "", isHline = False, parent = None):
        super(AQ_TabularCell, self).__init__(ctx, parent)
        self.width = len(content)
        self.colspan = 1
        self.rowspan = 1
        self.content = content.strip()
        self.isHline = isHline

    def __repr__(self):
        return f"<cell width='{self.width}'>\n"+ self.content +"\n</cell>"

    def __str__(self):
        return f"<cell width='{self.width}'>\n"+ self.content +"\n</cell>"