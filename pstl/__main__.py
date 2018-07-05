from typing import NewType
from pstl.ast.Visitor import Visitor
from AutoQcmVisitor import AutoQcmVisitor
from antlr4 import *
from AutoQcmLexer import AutoQcmLexer
from AutoQcmParser import AutoQcmParser
from pstl.ast.Headline import *
from pstl.ast.Comment import *
from pstl.ast.Directive import *


with open('input.rst', 'r') as rst_file:
    code = rst_file.read()

# This is the scary part that you don't need to worry about.

inputStream = InputStream(code)
l = AutoQcmLexer(inputStream)
tokenStream = CommonTokenStream(l)
p = AutoQcmParser(tokenStream)
p._errHandler = BailErrorStrategy()
p._interp.predictionMode = PredictionMode.SLL

def print_ast(ctx:RuleContext):
        explore(ctx, 0)

 
def explore(ctx, indentation):
    ruleName = AutoQcmParser.ruleNames[ctx.getRuleIndex()]


    print(("  " * indentation) + ruleName)
    

    for i in range(0, ctx.getChildCount()):
        element = ctx.getChild(i)
        if isinstance(element, RuleContext):
            explore(element, indentation + 1)


if __name__ == '__main__':


    # Parse and execute the code.
    #p._errHandler = BailErrorStrategy()
    cst = p.document()

    
    #print_ast(cst)
    ast = Visitor().visitDocument(cst)
    doc = ast.latex()
    doc.generate_pdf(clean_tex=False)

