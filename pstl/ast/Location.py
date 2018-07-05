from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.Token import Token, CommonToken
import AutoQcmParser

class Location(object):
    
    def __init__(self, ctx:ParserRuleContext):
        self.firstToken = ctx.start
        #self.filename = self.firstToken.getTokenSource().getSourceName()
        self.line = self.firstToken.line
        self.column = self.firstToken.column

    def __str__(self):
        print(f" - line : {self.line} | column : {self.column}")
