import unittest
from unittest.case import TestCase
from pstl.org.utils.parser import SyntaxMatcher
from pstl.org.nodes.comment import CommentNode

class Test_SyntaxMatcher(unittest.TestCase):

    def test_pattern_Options(self):
        matcher = SyntaxMatcher()
        self.assertTrue(matcher.matches("#+LANGUAGE: fr", 'OPTION'))

    def test_parser_Options(self):
        matcher = SyntaxMatcher()
        m = matcher.matches("#+LANGUAGE: fr", 'OPTION')
        name = m.group('name')
        value = m.group('value')
        self.assertTrue(name == 'LANGUAGE')
        self.assertTrue(value == 'fr')

    def test_pattern_Comment(self):
        matcher = SyntaxMatcher()
        self.assertTrue(matcher.matches("# LANGUAGE: fr", 'COMMENT'))

    def test_parser_Comment(self):
        matcher = SyntaxMatcher()
        m = matcher.matches("#Ceci est un commentaire de test", 'COMMENT')
        text = m.group('text')
        self.assertTrue(text == 'Ceci est un commentaire de test')

    def test_parser_Comment_Node(self):
        matcher = SyntaxMatcher()
        m = matcher.matches("#Ceci est un commentaire de test", 'COMMENT')
        text = m.group('text')
        node = CommentNode(None, text)
        self.assertTrue(node.toLatex() == '%Ceci est un commentaire de test')

    def test_pattern_Headline(self):
        matcher = SyntaxMatcher()
        m = matcher.matches("*** LANGUAGE: fr", 'HEADLINE')
        depth = len(m.group('level'))
        self.assertTrue(depth == 3)

if __name__ == '__main__':
    unittest.main()
