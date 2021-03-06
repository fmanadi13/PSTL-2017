# Generated from AutoQcmParser.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .AutoQcmParser import AutoQcmParser
else:
    from AutoQcmParser import AutoQcmParser

# This class defines a complete generic visitor for a parse tree produced by AutoQcmParser.

class AutoQcmParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AutoQcmParser#document.
    def visitDocument(self, ctx:AutoQcmParser.DocumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#headline.
    def visitHeadline(self, ctx:AutoQcmParser.HeadlineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#element.
    def visitElement(self, ctx:AutoQcmParser.ElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#directive.
    def visitDirective(self, ctx:AutoQcmParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#comment.
    def visitComment(self, ctx:AutoQcmParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#commentLineNoBreak.
    def visitCommentLineNoBreak(self, ctx:AutoQcmParser.CommentLineNoBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#commentLineAtoms.
    def visitCommentLineAtoms(self, ctx:AutoQcmParser.CommentLineAtomsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#listItemBullet.
    def visitListItemBullet(self, ctx:AutoQcmParser.ListItemBulletContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#bulletCrossLine.
    def visitBulletCrossLine(self, ctx:AutoQcmParser.BulletCrossLineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#bulletSimple.
    def visitBulletSimple(self, ctx:AutoQcmParser.BulletSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#bullet.
    def visitBullet(self, ctx:AutoQcmParser.BulletContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#listItemEnumerated.
    def visitListItemEnumerated(self, ctx:AutoQcmParser.ListItemEnumeratedContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabular.
    def visitTabular(self, ctx:AutoQcmParser.TabularContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabularRow.
    def visitTabularRow(self, ctx:AutoQcmParser.TabularRowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabularMixinCell.
    def visitTabularMixinCell(self, ctx:AutoQcmParser.TabularMixinCellContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabularCellHline.
    def visitTabularCellHline(self, ctx:AutoQcmParser.TabularCellHlineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabularCell.
    def visitTabularCell(self, ctx:AutoQcmParser.TabularCellContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#tabularCellContent.
    def visitTabularCellContent(self, ctx:AutoQcmParser.TabularCellContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#paragraph.
    def visitParagraph(self, ctx:AutoQcmParser.ParagraphContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#paragraphNoBreak.
    def visitParagraphNoBreak(self, ctx:AutoQcmParser.ParagraphNoBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lineNoBreak.
    def visitLineNoBreak(self, ctx:AutoQcmParser.LineNoBreakContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lines.
    def visitLines(self, ctx:AutoQcmParser.LinesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#linesNormal.
    def visitLinesNormal(self, ctx:AutoQcmParser.LinesNormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#linesEmphasis.
    def visitLinesEmphasis(self, ctx:AutoQcmParser.LinesEmphasisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lineNormal.
    def visitLineNormal(self, ctx:AutoQcmParser.LineNormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lineEmphasis.
    def visitLineEmphasis(self, ctx:AutoQcmParser.LineEmphasisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lineSpecial.
    def visitLineSpecial(self, ctx:AutoQcmParser.LineSpecialContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#spanLineStartNoEmphasis.
    def visitSpanLineStartNoEmphasis(self, ctx:AutoQcmParser.SpanLineStartNoEmphasisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#textLineStart.
    def visitTextLineStart(self, ctx:AutoQcmParser.TextLineStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#lineStart_fragment.
    def visitLineStart_fragment(self, ctx:AutoQcmParser.LineStart_fragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#text.
    def visitText(self, ctx:AutoQcmParser.TextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#textStart.
    def visitTextStart(self, ctx:AutoQcmParser.TextStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#spanNoEmphasis.
    def visitSpanNoEmphasis(self, ctx:AutoQcmParser.SpanNoEmphasisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#span.
    def visitSpan(self, ctx:AutoQcmParser.SpanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#text_fragment_start.
    def visitText_fragment_start(self, ctx:AutoQcmParser.Text_fragment_startContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#text_fragment.
    def visitText_fragment(self, ctx:AutoQcmParser.Text_fragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#emphasisText.
    def visitEmphasisText(self, ctx:AutoQcmParser.EmphasisTextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#emphasisAtoms.
    def visitEmphasisAtoms(self, ctx:AutoQcmParser.EmphasisAtomsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#emphasisNoSpace.
    def visitEmphasisNoSpace(self, ctx:AutoQcmParser.EmphasisNoSpaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#emphasisAtom.
    def visitEmphasisAtom(self, ctx:AutoQcmParser.EmphasisAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#hyperlink.
    def visitHyperlink(self, ctx:AutoQcmParser.HyperlinkContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#url.
    def visitUrl(self, ctx:AutoQcmParser.UrlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#urlAtom.
    def visitUrlAtom(self, ctx:AutoQcmParser.UrlAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#hyperlinkAtom.
    def visitHyperlinkAtom(self, ctx:AutoQcmParser.HyperlinkAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#latexEntity.
    def visitLatexEntity(self, ctx:AutoQcmParser.LatexEntityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#brackets.
    def visitBrackets(self, ctx:AutoQcmParser.BracketsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#latexFragment.
    def visitLatexFragment(self, ctx:AutoQcmParser.LatexFragmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#keyword.
    def visitKeyword(self, ctx:AutoQcmParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#indentation.
    def visitIndentation(self, ctx:AutoQcmParser.IndentationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#rawLineContent.
    def visitRawLineContent(self, ctx:AutoQcmParser.RawLineContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AutoQcmParser#empty_line.
    def visitEmpty_line(self, ctx:AutoQcmParser.Empty_lineContext):
        return self.visitChildren(ctx)



del AutoQcmParser