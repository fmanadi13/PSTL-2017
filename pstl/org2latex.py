from pstl.org.common import parser
from pstl.org.utils.latex import Latex
from pstl.org.common.parser import Parser
import os

def parseAndOutputHTML():
    parser = Parser()
    with open('pstl/test/samples/document.org', 'r') as myfile:
        orgCode = myfile.read()

    orgDocument = parser.parse(orgCode, {})
    orgLatexDocument = orgDocument['export'](Latex, {})
    #console.log(orgHTMLDocument.toString());
    print (orgLatexDocument)
    with open('output.tex','w') as f:
        f.write(orgLatexDocument)
    for node in orgDocument.nodes:

        print (node)


if __name__ == '__main__':
    parseAndOutputHTML()