import re
from pstl.org.utils.helper import Helper

class Syntax():
    rules = {}
    line = ''
    match = None

    def matches(line, linetype):
        Syntax.line = line
        Syntax.match = None

        try:
            pattern = Syntax.rules[linetype]
            Syntax.match = pattern.match(Syntax.line)
        except KeyError:
            pass

        return Syntax.match 

    def define(name, syntax):
        Syntax.rules[name] = syntax
        methodName = "is" + Helper._upper_first_letter(name)
        
        Helper._bind_method(Syntax, (lambda line : line and syntax.search(line) or False), methodName)


Syntax.define("directive", re.compile(r'^(?P<indent>\s*)#\+(?P<type>(begin|end)_)?(?P<content>.*)$', re.IGNORECASE))
Syntax.define("line", re.compile(r'^(?P<indent>\s*)(?P<content>.*)$'))
Syntax.define("comment", re.compile(r'^(?P<indent>\s*)#(?P<content>.*)'))
Syntax.define("option", re.compile(r'^#\+(?P<name>([A-Z_]+)):\s(?P<content>.*)$'))
Syntax.define("header", re.compile(r'^(?P<indent>\s*)(?P<level>\*+)\s+(?P<content>.+)$'))
Syntax.define("link", re.compile(r'\[\[(?P<url>https?://.+?)\](?:\[(?P<description>.+?)\])?\]'))
Syntax.define("tableRow", re.compile(r'^(?P<indent>\s*)\|(?P<content>.*?)\|?$'))
Syntax.define("blank", re.compile(r'^[\s]*$'))
Syntax.define("horizontalRule", re.compile(r'^\s*\-{5,}\s*'))

#Syntax.define("preformatted", /^(\s*):(?: (.*)$|$)/); // m[1] => indentation, m[2] => content
Syntax.define("unorderedListElement", re.compile('^(?P<indent>\s*)(-|\+|\s+\*)\s+(?P<content>.*)$'))
#Syntax.define("orderedListElement", /^(\s*)(\d+)(?:\.|\))\s+(.*)$/); // m[1] => indentation, m[2] => number, m[3] => content
Syntax.define("tableSeparator", re.compile('^(?P<indent>\s*)\|(?P<content>(?:\+|-)*?)\|?$'))




class Token():
    def isListElement(self):
        return self.type == Lexer.tokens['orderedListElement'] or self.type == Lexer.tokens['unorderedListElement']

    def isTableElement(self):
        return self.type == Lexer.tokens['tableSeparator'] or self.type == Lexer.tokens['tableRow']
    def isInternalLink(self):
        return True

class Lexer():
    tokens = {}
    def __init__(self, stream = None):
        self.stream = stream
        self.tokenStack = []
        for i, tokenName in enumerate([
          "directive",
          "header",
          "orderedListElement",
          "unorderedListElement",
          "link",
          "tableRow",
          "tableSeparator",
          "preformatted",
          "line",
          "horizontalRule",
          "blank",
          "option",
          "comment"
        ]):
           Lexer.tokens[tokenName] = i
  
    def tokenize(self, line):
        token = Token()
        if self.stream:
            token.fromLineNumber = self.stream.lineNumber
        else:
            token.fromLineNumber = 0

        if Syntax.isDirective(line):
            matches = Syntax.matches(line, 'directive')
            token.type        = Lexer.tokens['directive']
            token.indent      = len(matches.group('indent'))
            token.content     = matches.group('content')
            # On détermine s'il s'agit d'une directive linéaire ou un block
            directiveTypeString = matches.group('type')
            if (directiveTypeString and re.compile(r'^begin', re.IGNORECASE).search(directiveTypeString)):
                token.beginDirective = True
            elif (directiveTypeString and re.compile(r'^end', re.IGNORECASE).search(directiveTypeString)):
                token.endDirective = True
            else:
                token.oneshotDirective = True
        elif Syntax.isHeader(line):
            m = Syntax.matches(line, 'header')
            token.type        = Lexer.tokens['header']
            token.depth       = token.indent      = len(m.group('indent'))
            token.content     = m.group('content')
            #specific
            token.level       = len(m.group('level'))
        #elif Syntax.isPreformatted(line):
        #    token.type        = Lexer.tokens.preformatted
        #    token.indentation = RegExp.$1.length
        #    token.content     = RegExp.$2
        elif Syntax.isUnorderedListElement(line):
            m = Syntax.matches(line, 'unorderedListElement')
            token.type        = Lexer.tokens['unorderedListElement']
            token.indent      = len(m.group('indent'))
            token.content     = m.group('content')
        elif Syntax.isLink(line):
            m = Syntax.matches(line, 'link')
            token.type        = Lexer.tokens['link']
            token.url      = len(m.group('url'))
            token.content     = m.group('description')
        #elif Syntax.isOrderedListElement(line):
        #    token.type        = Lexer.tokens.orderedListElement
        #    token.indentation = RegExp.$1.length
        #    token.content     = RegExp.$3
        #    # specific
        #    token.number      = RegExp.$2
        elif Syntax.isTableSeparator(line):
            m = Syntax.matches(line, 'tableSeparator')
            token.type        = Lexer.tokens['tableSeparator']
            token.indent      = len(m.group('indent'))
            token.content     = m.group('content')
        elif Syntax.isTableRow(line):
            m = Syntax.matches(line, 'tableRow')
            token.type        = Lexer.tokens['tableRow']
            token.indent      = len(m.group('indent'))
            token.content     = m.group('content')
        elif Syntax.isBlank(line) or line == None:
            token.type        = Lexer.tokens['blank']
            token.indent      = 0
            token.content     = None
        elif Syntax.isHorizontalRule(line):
            m = Syntax.matches(line, 'horizontalRule')
            token.type        = Lexer.tokens['horizontalRule']
            token.indent      = len(m.group('indent'))
            token.content     = None
        elif Syntax.isComment(line):
            m = Syntax.matches(line, 'comment')
            token.type        = Lexer.tokens['comment']
            token.indent      = m.group('indent') and len(m.group('indent')) or 0
            token.content     = m.group('content')
        elif Syntax.isLine(line):
            m = Syntax.matches(line, 'line')
            token.type        = Lexer.tokens['line']
            token.indent      = len(m.group('indent'))
            token.content     = m.group('content')
        else:
            #raise ValidationError(f"SyntaxError: Unknown line: " + line)
            print ("Error: Empty line "+ line)

        return token
    
    def pushToken(self, token):
        self.tokenStack.append(token)

    def pushDummyTokenByType(self, type):
        token = Token()
        token.type = type
        self.tokenStack.append(token)
 
    def peekStackedToken(self):
        if len(self.tokenStack) > 0:
            return self.tokenStack[len(self.tokenStack) - 1]
        else:
            return None

    def getStackedToken(self):
        if len(self.tokenStack) > 0:
            return self.tokenStack.pop()
        else:
            return None

    def peekNextToken(self):
        return self.peekStackedToken() or self.tokenize(self.stream.peekNextLine())


    def getNextToken(self):
        return self.getStackedToken() or self.tokenize(self.stream.getNextLine())

    def hasNext(self):
        return self.stream.hasNext()

    def getLineNumber(self):
        return self.stream.lineNumber
