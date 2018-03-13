# -*- coding: utf-8 -*-
import re
from builtins import print
from pstl.org.nodes.base import BaseNode
from pstl.org.nodes.headline import HeadlineNode
from pstl.org.nodes.comment import CommentNode
from pstl.org.nodes.text import *

 
__all__ = ['SyntaxMatcher','SyntaxMatcher.match']
 


class SyntaxMatcher:
    ## List of regexes
    RE = {
        'OPTION'            : re.compile(r'^#\+(?P<name>([A-Z_]+)):\s(?P<value>.*)$'),
        'COMMENT'           : re.compile(r'^#(?P<text>.*)'),
        'BEGIN_QUESTIONS'   : re.compile(r'#\+BEGIN_QUESTIONS$'),
        'END_QUESTIONS'     : re.compile(r'#\+END_QUESTIONS$'),
        'HEADLINE'          : re.compile(r'(?P<level>\*+)\s+(?P<title>.+)$'),
        'ULIST'             : re.compile(r'(?P<depth>\s*)(-|\+)\s+(?P<item>.+)$'),
        'OLIST'             : re.compile(r'(?P<depth>\s*)\d+(\.|\))\s+(?P<item>.+)$'),
        'DEF_LIST'          : re.compile(r'(?P<depth>\s*)(-|\+)\s+(?P<item>.+?)\s*::\s*(?P<desc>.+)$'),
        'HRULE'             : re.compile(r'^\s*\-{5,}\s*'),
        'EMPTYLINE'         : re.compile(r'^\s*$'),
        'TEXT'              : re.compile(r'^(\s*)(.*)$'),
        'WHITELINE'         : re.compile(r'\s*$'),
        'SRC_BEGIN'         : re.compile(r'#\+BEGIN_SRC(?P<spc> )?(?(spc)\s*(?P<src_type>.+)|)$'),
        'SRC_END'           : re.compile(r'#\+END_SRC'),
        'TABLE_ROW'         : re.compile(r'\s*\|(?P<cells>(.+\|)+)s*$')
          }

    def __init__(self):
        self.line = ''
        self.match = None

    def matches(self, line, linetype):

        self.line = line
        self.match = None

        try:
            pattern = self.RE[linetype]
            self.match = pattern.match(line)
        except KeyError:
            pass

        return self.match 


class Parser(BaseNode):
    def __init__(self, text, default_heading=1):
        self.text    = text
        self.matcher = SyntaxMatcher()
        self.ast     = BaseNode()
        self.root    = self.ast
        self.children = []
        self.parent = self
        self.current = self
        self.questions_flg = False
        self.bquote_flg = False
        self.src_flg = False
        self.default_heading = default_heading
        self._parse(self.text)

    def _parse(self, text):
        text = text.splitlines()
        for line in text:
            if self.src_flg and not self.regexps['src_end'].match(line):
                self.current.append(Text(line, noparse=True))
                continue
            if re.match(SyntaxMatcher.RE['COMMENT'], line):
                m = matcher.matches(line, 'COMMENT')
                text = m.group('text')
                node = CommentNode(self.current, text)
                self.current.push(node)
                self.current = node

            elif re.match(SyntaxMatcher.RE['HEADLINE'], line):
                m = matcher.matches(line, 'HEADLINE')
                while (not isinstance(self.current, HeadlineNode)):
                    self.current = self.current.parent
                self._add_heading_node(Heading(
                    depth=len(m.group('level')),
                    title=m.group('title'),
                    default_depth=self.default_heading))
            elif re.match(SyntaxMatcher.RE['BEGIN_QUESTIONS'], line):
                self.questions_flg = True
                m = matcher.matches(line, 'BEGIN_QUESTIONS')

                node = QuestionsNode()
                self.current.append(node)
                self.current = node
            elif re.match(SyntaxMatcher.RE['END_QUESTIONS'], line):
                if not self.questions_flg:
                    raise NestingNotValidError
                self.questions_flg = False
                while not isinstance(self.current, QuestionsNode):
                    if isinstance(self.current, Org):
                        raise NestingNotValidError
                    self.current = self.current.parent
                self.current = self.current.parent
            #elif self.regexps['orderedlist'].match(line):
            #    while isinstance(self.current, Paragraph):
            #        self.current = self.current.parent
            #    m = self.regexps['orderedlist'].match(line)
            #    self._add_olist_node(m)
            #elif self.regexps['definitionlist'].match(line):
            #    while isinstance(self.current, Paragraph):
            #        self.current = self.current.parent
            #    m = self.regexps['definitionlist'].match(line)
            #    self._add_dlist_node(m)
            #elif self.regexps['unorderedlist'].match(line):
            #    while isinstance(self.current, Paragraph):
            #        self.current = self.current.parent
            #    m = self.regexps['unorderedlist'].match(line)
            #    self._add_ulist_node(m)
            #elif self.regexps['tablerow'].match(line):
            #    m = self.regexps['tablerow'].match(line)
            #    self._add_tablerow(m)
            elif not line:
                if isinstance(self.current, ParagraphNode):
                    self.current = self.current.parent
            elif (not isinstance(self.current, HeadlineNode) and
                  isinstance(self.current, BaseNode)):
                self.current.push(TextNode(line))
            else:
                node = ParagraphNode()
                self.current.push(node)
                self.current = node
                self.current.push(TextNode(line))
        if self.bquote_flg or self.src_flg or self.questions_flg:
            raise NestingNotValidError

        def _get_open(self, to = 'latex'):
            return ''
        def _get_close(self, to = 'latex'):
            '''returns latex close tag str'''
            return ''


if __name__ == "__main__":
    matcher = SyntaxMatcher()
    parser = Parser("# Commentaire à parser")
    parser._parse("# Commentaire à parser")
    print (parser.toLatex())