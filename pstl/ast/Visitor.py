from AutoQcmVisitor import AutoQcmVisitor
from pstl.ast.Paragraph import AQ_Emphasis
from pstl.ast.Paragraph import AQ_Paragraph, AQ_Line, AQ_LatexEntity, AQ_Span, AQ_Text
from pstl.ast.Lists import AQ_Item, AQ_Checkboxes
from AutoQcmParser import AutoQcmParser
from pstl.ast.Tabular import *
from pstl.ast.Comment import AQ_Comment
from pstl.ast.Directive import AQ_Directive
from pstl.ast.EmptyLine import AQ_EmptyLine
from pstl.ast.Headline import AQ_Headline
from pstl.ast.Document import AQ_Document
from pstl.ast.Reference import AQ_Reference
from pstl.ast.Figure import AQ_Figure
from pstl.ast.LatexFragment import AQ_LatexFragment

class Visitor(AutoQcmVisitor):

        # Visit a parse tree produced by AutoQcmParser#document.
    def visitDocument(self, ctx:AutoQcmParser.DocumentContext):
        doc = AQ_Document(ctx)
        __current_list = None
        for element in ctx.element():
            item = self.visitElement(element)
            # Debut d'une liste
            if isinstance(item, AQ_Item):
                if __current_list == None:
                    __current_list = AQ_Checkboxes(ctx, doc)
                item.parent = __current_list
                __current_list.append(item)
            else:
                if __current_list:
                    doc.appendChild(__current_list)
                    __current_list = None
                item.parent = doc
                doc.appendChild(item)
        return doc


    # Visit a parse tree produced by AutoQcmParser#headline.
    def visitHeadline(self, ctx:AutoQcmParser.HeadlineContext):
        return  AQ_Headline(ctx, 0, len(ctx.level().getText()), ctx.title.getText())


    # Visit a parse tree produced by AutoQcmParser#element.
    def visitElement(self, ctx:AutoQcmParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#empty_line.
    def visitEmpty_line(self, ctx:AutoQcmParser.Empty_lineContext):
        return AQ_EmptyLine(ctx)


    # Visit a parse tree produced by AutoQcmParser#directive.
    def visitDirective(self, ctx:AutoQcmParser.DirectiveContext):

        return AQ_Directive(ctx, ctx.name.getText(), ctx.value.getText())


    # Visit a parse tree produced by AutoQcmParser#comment.
    def visitComment(self, ctx:AutoQcmParser.CommentContext):
        return AQ_Comment(ctx, ctx.content.getText())
    # Visit a parse tree produced by AutoQcmParser#document.
    def visitListItemBullet(self, ctx:AutoQcmParser.ListItemBulletContext):
        return self.visitChildren(ctx)
    def visitBulletSimple(self, ctx:AutoQcmParser.BulletSimpleContext):
        _itemlist = AQ_Item(ctx)
        _isChecked = False
        _is_checked_content = None
        if ctx.checkBox():
            _is_checked_content = ctx.checkBox().getText()
            _isChecked = True if _is_checked_content.strip().lower() == '[x]' else False
        _itemlist.isChecked = _isChecked
        _paragraphNoBreak = self.visitParagraphNoBreak(ctx.paragraphNoBreak())
        _paragraphNoBreak.parent = _itemlist
        _itemlist.appendChild(_paragraphNoBreak)
        _paragraph = None
        for p in ctx.paragraph():
            _paragraph = self.visitParagraph(p)
            _paragraph.parent = _itemlist
            _itemlist.appendChild(_paragraph)
            
        return _itemlist
    # Visit a parse tree produced by AutoQcmParser#document.
    def visitListItemEnumerated(self, ctx:AutoQcmParser.ListItemEnumeratedContext):

        return AQ_Item(ctx)
    # Visit a parse tree produced by AutoQcmParser#tabular.
    def visitTabular(self, ctx:AutoQcmParser.TabularContext):
        tab = AQ_Tabular(ctx)
        for row in ctx.tabularRow():
            item = self.visitTabularRow(row)
            item.parent = tab
            tab.appendChild(item)
        return tab


    # Visit a parse tree produced by AutoQcmParser#tabularRow.
    def visitTabularRow(self, ctx:AutoQcmParser.TabularRowContext):
        tabRow = AQ_TabularRow(ctx)
        if ctx.tabularCellHline():
            cell = ctx.tabularCellHline()
            item = self.visitTabularCellHline(cell)
            tabRow.hasHline = True
            item.parent = tabRow
            tabRow.appendChild(item)
        for cell in ctx.tabularMixinCell():
            item = self.visitTabularMixinCell(cell)
            if item.isHline:
                tabRow.hasHline = True
            item.parent = tabRow
            tabRow.appendChild(item)
        if tabRow.children[0].isHline:
            tabRow.children[0].width = tabRow.children[0].width +1
        return tabRow

    def visitTabularMixinCell(self, ctx:AutoQcmParser.TabularCellHlineContext):
        if ctx.tabularCellHline():
            return self.visitTabularCellHline(ctx.tabularCellHline())
        elif ctx.tabularCell():
            return self.visitTabularCell(ctx.tabularCell())

    # Visit a parse tree produced by AutoQcmParser#tabularCellHline.
    def visitTabularCellHline(self, ctx:AutoQcmParser.TabularCellHlineContext):
        _content = ''.join([c.text for c in ctx.content])
        _isHline = True
        return AQ_TabularCell(ctx, _content, _isHline)


    # Visit a parse tree produced by AutoQcmParser#tabularCell.
    def visitTabularCell(self, ctx:AutoQcmParser.TabularCellContext):
        #a = ctx.start.getStartIndex()
        #b = ctx.stop.getStopIndex()
        #interval = Interval(a,b)
        #input = ctx.start.getInputStream()
        return AQ_TabularCell(ctx, ctx.content.getText())


    # Visit a parse tree produced by AutoQcmParser#paragraph.
    def visitParagraph(self, ctx:AutoQcmParser.ParagraphContext):
        _paragraph = AQ_Paragraph(ctx)
        for line in ctx.line():
            _line = self.visitLine(line)
            _line.parent = _paragraph
            _paragraph.appendChild(_line)

        return _paragraph
    def visitParagraphNoBreak(self, ctx:AutoQcmParser.ParagraphNoBreakContext):
        _paragraph = AQ_Paragraph(ctx)
        _line = ctx.lineNoBreak()
        _lineNoBreak = self.visitLineNoBreak(_line)
        _lineNoBreak.parent = _paragraph
        _paragraph.appendChild(_lineNoBreak)

        return _paragraph

    # Visit a parse tree produced by AutoQcmParser#paragraph.
    def visitLine(self, ctx:AutoQcmParser.LineContext):
        _line = AQ_Line(ctx)
        for span in ctx.span():
            _span = self.visitSpan(span)
            _span.parent = _line
            _line.appendChild(_span)

        return _line
    def visitLineNoBreak(self, ctx:AutoQcmParser.LineNoBreakContext):
        _line = AQ_Line(ctx)
        for span in ctx.span():
            _span = self.visitSpan(span)
            _span.parent = _line
            _line.appendChild(_span)

        return _line
        # Visit a parse tree produced by AutoQcmParser#paragraph.
    def visitSpan(self, ctx:AutoQcmParser.SpanContext):
        return self.visitChildren(ctx)

    def visitHyperlink(self, ctx:AutoQcmParser.HyperlinkContext):
        _url = ctx.url().getText()
        if _url.lower().endswith(('.png', '.jpg', '.jpeg')):
            return AQ_Figure(ctx, _url)
        else:
            return AQ_Reference(ctx, _url)

    def visitLatexEntity(self, ctx:AutoQcmParser.LatexEntityContext):
        _entity_name = ctx.name()
        return AQ_LatexEntity(ctx, _entity_name)


    def visitLatexFragment(self, ctx:AutoQcmParser.LatexFragmentContext):
        _content = ''.join([c.text for c in ctx.content])
        _delimiter = None
        if ctx._ESC_C_PAREN:
            _delimiter = "\("
        elif ctx.DOLLAR:
            _delimiter = "$"
        elif ctx._ESC_C_S_BRACKET:
            _delimiter = "\["

        return AQ_LatexFragment(ctx, _content)


    def visitEmphCode(self, ctx:AutoQcmParser.EmphCodeContext):
        return None


    def visitEmphVerbatim(self, ctx:AutoQcmParser.EmphVerbatimContext):
        return None


    def visitEmphasis(self, ctx:AutoQcmParser.EmphasisContext):
        _delimiter = None
        _child = None
        if ctx.SLASH():
            _delimiter = '/'
        elif ctx.STAR():
            _delimiter = '*'
        _emphasis = AQ_Emphasis(ctx, _delimiter)
        for childCtx in ctx.children:
            if isinstance(childCtx, AutoQcmParser.EmphasisContext):
                _child = self.visitEmphasis(childCtx)
                _emphasis.appendChild(_child)
                _child.parent = _emphasis
            elif isinstance(childCtx, AutoQcmParser.TextContext):
                _child = self.visitText(childCtx)
                _emphasis.appendChild(_child)
                _child.parent = _emphasis
        return _emphasis


    def visitText(self, ctx:AutoQcmParser.TextContext):
        return self.visitChildren(ctx)

    def visitLineStart_fragment(self, ctx:AutoQcmParser.LineStart_fragmentContext):
        _content = ctx.getText()
        return AQ_Text(ctx, _content)

    
    def visitText_fragment_start(self, ctx:AutoQcmParser.Text_fragment_startContext):
        _content = ctx.getText()
        return AQ_Text(ctx, _content)

    def visitText_fragment(self, ctx):
        return super().visitText_fragment(ctx)