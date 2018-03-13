import unittest
from pstl.org.common.lexer import Lexer


class Test_test_lexer(unittest.TestCase):
    def test_tokenize_option(self):
        lexer = Lexer()
        token = lexer.tokenize("#+AUTHOR: FARES MANADI")
        self.assertTrue(token.type == Lexer.tokens['option'])
        self.assertTrue(token.name == "AUTHOR")
        self.assertTrue(token.content == "FARES MANADI")

    def test_tokenize_comment(self):
        lexer = Lexer()
        token = lexer.tokenize("# AUTHOR: FARES MANADI")
        self.assertTrue(token.type == Lexer.tokens['comment'])
        self.assertTrue(token.content == " AUTHOR: FARES MANADI")

    def test_tokenize_header(self):
        lexer = Lexer()    
        token = lexer.tokenize("** AUTHOR: FARES MANADI")
        print (token.content)
        self.assertTrue(token.type == Lexer.tokens['header'])
        self.assertTrue(token.content == "AUTHOR: FARES MANADI")
        self.assertTrue(token.level == 2)

if __name__ == '__main__':
    unittest.main()
