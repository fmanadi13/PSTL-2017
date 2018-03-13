import re
from _collections import deque

from pstl.org.common.stream import Stream
from pstl.org.common.node import Node
from pstl.org.common.lexer import Lexer
from pstl.org.common.lexer import Syntax

__all__ = ['parse']

class Parser():
    inlineParser = None
    definitionPattern = re.compile('^(?P<defname>.*?) :: *(?P<content>.*)$')
    checkboxPattern = re.compile('^\s*?(?P<isCheckbox>\[(?P<checked>\+|-|x|\s*)\])(?P<content>.*)$', re.IGNORECASE)
    unknownDefinitionTerm = "???"
    def __init__(self):
        self.options = {}
        self.dLocal = False
        self.inlineParser = InlineParser()

    def initStatus(self, stream, options):
        if isinstance(stream,  str):
            stream = Stream(stream)
        self.lexer = Lexer(stream)
        self.nodes = []
        self.options = {
          "toc": False,
          "num": True,
          "^": "{}",
          "multilineCell": False
        }
        # Override option values
        if options and isinstance(options, object):
            for key in options:
                self.options[key] = options[key]

        self.document = {
            "directives":{
                "global": {
                    "options": {},
                    "metadata": {},
                    "latex": {},
                    "export": {}
                },
                "local": {}
                },
            "export": (lambda ExporterClass, exportOptions: ExporterClass(self, exportOptions).output)
        }

    def parse(self, stream, options = {}):
        self.initStatus(stream, options)
        self.parseDocument()
        self.document['nodes'] = self.nodes
        return self.document

    def createErrorReport(self, message):
        print(message + " at line " + str(self.lexer.getLineNumber()))

    def skipBlank(self):
        blankToken = None
        while self.lexer.peekNextToken().type == Lexer.tokens['blank']:
            blankToken = self.lexer.getNextToken()
        return blankToken
    @staticmethod
    def setNodeOriginFromToken(node, token):
        node.fromLineNumber = token.fromLineNumber
        return node

    def appendNode(self, newNode):
        previousSibling = len(self.nodes) > 0 and self.nodes[len(self.nodes) - 1] or None
        self.nodes.append(newNode)
        newNode.previousSibling = previousSibling
    
    # ------------------------------------------------------------
    # <Document> ::= <Element>*
    # ------------------------------------------------------------

    def parseDocument(self):
        #self.parseTitle()
        self.parseNodes()

    def parseNodes(self):
        while self.lexer.hasNext():
            element = self.parseElement()
            if element:
                self.appendNode(element)

    def parseTitle(self):
        self.skipBlank()
        if self.lexer.hasNext() and self.lexer.peekNextToken().type == Lexer.tokens['line']:
            self.document.title = self.createTextNode(self.lexer.getNextToken().content)
        else:
            self.document.title = None

        self.lexer.pushDummyTokenByType(Lexer.tokens['blank'])

    # ------------------------------------------------------------
    # <Element> ::= (<Header> | <List>
    #              | <Preformatted> | <Paragraph>
    #              | <Table>)*
    # ------------------------------------------------------------

    def parseElement(self):
        element = None
        if self.lexer.peekNextToken().type == Lexer.tokens['directive']:
            element = self.parseDirective()
        else:
            self.dLocal = True
            if self.lexer.peekNextToken().type == Lexer.tokens['header']:
                element = self.parseHeader()
            elif self.lexer.peekNextToken().type == Lexer.tokens['link']:
                element = self.parseLink()
            elif self.lexer.peekNextToken().type == Lexer.tokens['preformatted']:
                element = self.parsePreformatted()
            elif self.lexer.peekNextToken().type == Lexer.tokens['orderedListElement'] or self.lexer.peekNextToken().type ==  Lexer.tokens['unorderedListElement']:
                element = self.parseList()
            elif self.lexer.peekNextToken().type == Lexer.tokens['line']:
                element = self.parseText()
            elif self.lexer.peekNextToken().type == Lexer.tokens['tableRow'] or self.lexer.peekNextToken().type == Lexer.tokens['tableSeparator']:
                element = self.parseTable()
            elif self.lexer.peekNextToken().type == Lexer.tokens['blank']:
                self.skipBlank()
                if self.lexer.hasNext():
                    if self.lexer.peekNextToken().type == Lexer.tokens['line']:
                        element = self.parseParagraph()
                    else:
                        element = self.parseElement()
            elif self.lexer.peekNextToken().type == Lexer.tokens['horizontalRule']:
                self.lexer.getNextToken()
                element = Node.createHorizontalRule()
            elif self.lexer.peekNextToken().type == Lexer.tokens['comment']:
                # Skip
                self.lexer.getNextToken()
            else:
                self.createErrorReport("Unhandled token: " + str(self.lexer.peekNextToken().type))

        return element

    def parseElementBesidesDirectiveEnd(self):
        try:
          # Temporary, override the definition of `parseElement`
          self.parseElement = self.parseElementBesidesDirectiveEndBody
          return self.parseElement()
        finally:
          self.parseElement = self.originalParseElement

    def parseElementBesidesDirectiveEndBody(self):
        if self.lexer.peekNextToken().type == Lexer.tokens['directive'] and hasattr(self.lexer.peekNextToken(), 'endDirective'):
            return None
        return self.originalParseElement()


    # ------------------------------------------------------------
    # <Directive> ::= "#+.*"
    # ------------------------------------------------------------

    def parseDirective(self):
        directiveToken = self.lexer.getNextToken()
        directiveNode = self.createDirectiveNodeFromToken(directiveToken)

        if hasattr(directiveToken, 'endDirective'):
            self.createErrorReport("Unmatched 'end' directive for " + directiveNode.directiveName)

        if hasattr(directiveToken, 'oneshotDirective'):
            self.interpretDirective(directiveNode)
            return directiveNode

        if not hasattr(directiveToken, 'beginDirective'):
            self.createErrorReport("Invalid directive " + directiveNode.directiveName)

        # Parse begin ~ end
        directiveNode.children = []
        if self.isVerbatimDirective(directiveNode):
            return self.parseDirectiveBlockVerbatim(directiveNode)
        else:
            return self.parseDirectiveBlock(directiveNode)


    def createDirectiveNodeFromToken(self, directiveToken):
        matched = re.compile('^\s*(?P<name>[^\s:]*)[\s]*(?P<raw>.*)\s*$').match(directiveToken.content)
        directiveNode = Node.createDirective(None, {})
        self.setNodeOriginFromToken(directiveNode, directiveToken)
        directiveNode.directiveName = matched.group('name').lower()
        directiveNode.directiveArguments = self.parseDirectiveArguments(matched.group('raw'))
        directiveNode.directiveOptions = self.parseDirectiveOptions(matched.group('raw'))
        directiveNode.directiveRawValue = directiveNode.value = matched.group('raw')

        return directiveNode

    @staticmethod
    def isVerbatimDirective(directiveNode):
        directiveName = directiveNode.directiveName
        return directiveName == "src" or directiveName == "example" or directiveName == "html"


    def parseDirectiveBlock(self, directiveNode, verbatim = None):
        self.lexer.pushDummyTokenByType(Lexer.tokens['blank'])

        while self.lexer.hasNext():
            nextToken = self.lexer.peekNextToken()
            if nextToken.type == Lexer.tokens['directive'] and hasattr(nextToken, 'endDirective') and self.createDirectiveNodeFromToken(nextToken).directiveName == directiveNode.directiveName:
                # Close directive
                self.lexer.getNextToken()
                return directiveNode
            element = self.parseElementBesidesDirectiveEnd()
            if element:
                directiveNode.appendChild(element)

        raise self.createErrorReport("Unclosed directive " + directiveNode.directiveName)


    def parseDirectiveBlockVerbatim(self, directiveNode):
        textContent = []

        while self.lexer.hasNext():
            nextToken = self.lexer.peekNextToken()
            if nextToken.type == Lexer.tokens['directive'] and hasattr(nextToken, 'endDirective') and self.createDirectiveNodeFromToken(nextToken).directiveName == directiveNode.directiveName:
                self.lexer.getNextToken()
                directiveNode.appendChild(self.createTextNode(textContent.join("\n"), True))
                return directiveNode
            textContent.append(self.lexer.stream.getNextLine())
    

        raise self.createErrorReport("Unclosed directive " + directiveNode.directiveName)

    @staticmethod
    def parseDirectiveArguments(parameters):
        splitedParameters = parameters.split(r'[\s]+')
        return filter(lambda param: len(param) and param[0] != "-", splitedParameters)
        
    @staticmethod
    def parseDirectiveOptions(parameters):
        splitedParameters = parameters.split(r'[\s]+')
        return filter(lambda param: len(param) and param[0] == "-", splitedParameters)


    def interpretDirective(self, directiveNode):
        # http://orgmode.org/manual/Export-options.html
        if directiveNode.directiveName == "options":
            self.interpretOptionDirective(directiveNode)
        elif re.compile(r'^export_', re.IGNORECASE).search(directiveNode.directiveName):
            print ("export directive")
        elif re.compile(r'^latex_', re.IGNORECASE).search(directiveNode.directiveName):
            if directiveNode.directiveName.upper() == "LATEX_HEADER":
                if hasattr(self.document['directives']['global']['latex'], 'header'):
                    self.document['directives']['global']['latex']['header'] += "\n" + directiveNode.directiveRawValue
                else:
                    print('Test')
            else:
                print ("Test")
        else:
            if directiveNode.directiveName.upper() == "DESCRIPTION":
                if hasattr(self.document['directives']['global']['metadata'], 'description'):
                    self.document['directives']['global']['metadata']['description'] += "\n" + directiveNode.directiveRawValue
                else:
                    self.document['directives']['global']['metadata'][directiveNode.directiveName] = directiveNode.directiveRawValue
            else:
                self.document['directives']['global']['metadata'][directiveNode.directiveName] = directiveNode.directiveRawValue



    def interpretOptionDirective(self, optionDirectiveNode):
        for pairString in optionDirectiveNode.directiveArguments:
            pair = pairString.split(":")
            self.document['directives']['global']['options'][pair[0]] = self.convertLispyValue(pair[1])


    def convertLispyValue(lispyValue):
    
        if lispyValue == "t":
            return True
        elif lispyValue == "nil":
            return False
        else:
            if r'/^[0-9]+$'.test(lispyValue):
                return parseInt(lispyValue)
            return lispyValue


    # ------------------------------------------------------------
    # <Header>
    #
    # : preformatted
    # : block
    # ------------------------------------------------------------

    def parseHeader(self):
        headerToken = self.lexer.getNextToken()
        
        header = Node.createHeader([
            self.createTextNode(headerToken.content) # TODO: Parse inline markups
        ], { 'level': headerToken.level , 'value': headerToken.content})
        self.setNodeOriginFromToken(header, headerToken)

        return header
    # ------------------------------------------------------------
    # <Link>
    # ------------------------------------------------------------

    def parseLink(self):
        linkToken = self.lexer.getNextToken()
        
        link = Node.createLink([
            self.createTextNode(linkToken.content) # TODO: Parse inline markups
        ], { 'url': linkToken.url})
        self.setNodeOriginFromToken(link, linkToken)

        return link
    # ------------------------------------------------------------
    # <Option>
    #
    # : directive
    # ------------------------------------------------------------

    def parseOption(self):
        optionToken = self.lexer.getNextToken()
        option = Node.createOption([
            self.createTextNode(optionToken.content) # TODO: Parse inline markups
        ], { 'name': optionToken.name })
        self.setNodeOriginFromToken(option, optionToken)

        return option

    # ------------------------------------------------------------
    # <Preformatted>
    #
    # : preformatted
    # : block
    # ------------------------------------------------------------
    def parsePreformatted(self):
        preformattedFirstToken = self.lexer.peekNextToken()
        preformatted = Node.createPreformatted([])
        self.setNodeOriginFromToken(preformatted, preformattedFirstToken)

        textContents = []

        while self.lexer.hasNext():
            token = self.lexer.peekNextToken()
            if token.type != Lexer.tokens['preformatted'] or token.indent < preformattedFirstToken.indent:
                break
            self.lexer.getNextToken()
            textContents.append(token.content)

        preformatted.appendChild(self.createTextNode(textContents.join("\n"), True))

        return preformatted

    # ------------------------------------------------------------
    # <List>
    #
    #  - foo
    #    1. bar
    #    2. baz
    # ------------------------------------------------------------

    # XXX: not consider codes (e.g., =Foo::Bar=)
    
    
    def parseList(self):
        rootToken = self.lexer.peekNextToken()
        list = []
        isDefinitionList = False
        isCheckboxList = False
        if re.search(Parser.definitionPattern, rootToken.content):
            list = Node.createDefinitionList([])
            isDefinitionList = True
        elif re.search(Parser.checkboxPattern, rootToken.content):
            list = Node.createCheckboxList([])
            isCheckboxList = True
        else:
            if rootToken.type == Lexer.tokens['unorderedListElement']:
                list = Node.createUnorderedList([])
            else:
                list = Node.createOrderedList([])
   
        self.setNodeOriginFromToken(list, rootToken)

        while self.lexer.hasNext():
            nextToken = self.lexer.peekNextToken()
            if not nextToken.isListElement() or nextToken.indent != rootToken.indent:
                break
            list.appendChild(self.parseListElement(rootToken.indent, isDefinitionList, isCheckboxList))

        
        return list


    

    def parseListElement(self, rootIndentation, isDefinitionList, isCheckboxList):
        listElementToken = self.lexer.getNextToken()
        listElement = Node.createListElement([])
        self.setNodeOriginFromToken(listElement, listElementToken)

        listElement.isDefinitionList = isDefinitionList
        listElement.isCheckboxList = isCheckboxList
        if isDefinitionList:
            match = re.match(Parser.definitionPattern, listElementToken.content)
            listElement.term = [self.createTextNode(match and (match.group('defname') and match.group('defname') or self.unknownDefinitionTerm))]
            listElement.appendChild(self.createTextNode(match and match.group('content') or listElementToken.content))
        
        elif isCheckboxList:
            match = re.match(Parser.checkboxPattern, listElementToken.content)
            if match:
                if match.group('checked').lower() == '+' or match.group('checked').lower() == 'x' or match.group('checked').lower() == '-':
                    listElement.isChecked = True
                else:
                    listElement.isChecked = False
            listElement.appendChild(self.createTextNode(match and match.group('content') or listElementToken.content))
        else:
            listElement.appendChild(self.createTextNode(listElementToken.content))

        while self.lexer.hasNext():
            blankToken = self.skipBlank()
            if not self.lexer.hasNext():
                break

            notBlankNextToken = self.lexer.peekNextToken()
            if not notBlankNextToken.isListElement():
                # Recover blank token only when next line is not listElement.
                None
                # self.lexer.pushToken(blankToken)
                #end of the list
            
            if notBlankNextToken.indent <= rootIndentation:
                break
            #recursive
            element = self.parseElement()
            if element:
                listElement.appendChild(element)


        return listElement
 

    # ------------------------------------------------------------
    # <Table> ::= <TableRow>+
    # ------------------------------------------------------------

    def parseTable(self):
        nextToken = self.lexer.peekNextToken()
        table = Node.createTable([],{})
        self.setNodeOriginFromToken(table, nextToken)
        sawSeparator = False

        allowMultilineCell = Lexer.tokens['tableSeparator'] and self.options['multilineCell']
        nextToken.type == Lexer.tokens['tableSeparator'] and self.options['multilineCell']

        if self.lexer.hasNext():
            nextToken = self.lexer.peekNextToken()
        while self.lexer.hasNext() and nextToken.isTableElement():
            if nextToken.type == Lexer.tokens['tableRow']:
                tableRow = self.parseTableRow(allowMultilineCell)
                table.appendChild(tableRow)
            else:
                # Lexer.tokens.tableSeparator
                sawSeparator = True


            if sawSeparator and len(table.children):
                for cell in table.children[0].children:
                    cell.isHeader = True

            self.lexer.getNextToken()
            nextToken = self.lexer.peekNextToken()
               
        return table

    # ------------------------------------------------------------
    # <TableRow> ::= <TableCell>+
    # ------------------------------------------------------------

    def parseTableRow (self, allowMultilineCell):
        tableRowTokens = deque([])
        i = 0
        while self.lexer.peekNextToken().type == Lexer.tokens['tableRow']:
            tableRowTokens.append(self.lexer.getNextToken())
            if not allowMultilineCell:
                break

        if not len(tableRowTokens):
            self.createErrorReport("Expected table row")
  
        firstTableRowToken = tableRowTokens.popleft()
        tableCellTexts = firstTableRowToken.content.split("|")

        for rowToken in tableRowTokens:
            rowTokenParts = rowToken.content.split("|")
            for (cellIdx, cellText) in enumerate(rowTokenParts):
                tableCellTexts[cellIdx] = cellText

        for cell in tableCellTexts:
            print (cell)

        tableCells = []
        for i in range(0, len(tableCellTexts)):
            tableCells.append(Node.createTableCell([Parser.createTextNode(tableCellTexts[i], True)], {"value": tableCellTexts[i]}))
        # TODO: Prepare two pathes: (1)

        return self.setNodeOriginFromToken(Node.createTableRow(tableCells), firstTableRowToken)


    # ------------------------------------------------------------
    # <Paragraph> ::= <Blank> <Line>*
    # ------------------------------------------------------------

    def parseParagraph(self):
        paragraphFisrtToken = self.lexer.peekNextToken()
        paragraph = Node.createParagraph([],{})
        self.setNodeOriginFromToken(paragraph, paragraphFisrtToken)

        textContents = []

        while self.lexer.hasNext():
            nextToken = self.lexer.peekNextToken()
            if nextToken.type != Lexer.tokens['line'] or nextToken.indent < paragraphFisrtToken.indent:
                break
            self.lexer.getNextToken()
            textContents.append(nextToken.content)

        paragraph.appendChild(self.createTextNode("\n".join(textContents)))

        return paragraph


    def parseText(self, noEmphasis = True):
        lineToken = self.lexer.getNextToken()
        return self.createTextNode(lineToken.content,noEmphasis)

    # ------------------------------------------------------------
    # <Text> (DOM Like)
    # ------------------------------------------------------------

    def createTextNode(self, text, noEmphasis = True):
        return (noEmphasis and Node.createText(None, { "value": text })) or self.inlineParser.parseEmphasis(text)
 


# ------------------------------------------------------------
# Parser for Inline Elements
#
# @refs org-emphasis-regexp-components
# ------------------------------------------------------------

class InlineParser():
    def __init__(self):
        self.depth = 0
        self.preEmphasis     = " \t\\('\""
        self.postEmphasis    = "- \t.,:!?;'\"\\)"
        self.borderForbidden = " \t\r\n,\"'"
        self.bodyRegexp      = "[\\s\\S]*?"
        self.markers         = "*/_=~+"
        # \1 => link, \2 => text
        self.linkPattern = r'\[\[([^\]]*)\](?:\[([^\]]*)\])?\]' #g
        self.emphasisPattern = self.buildEmphasisPattern()
        

    def parseEmphasis(self, text):
        emphasisPattern = self.emphasisPattern
        emphasisPattern.lastIndex = 0

        result = []
        match
        previousLast = 0
        savedLastIndex

        match = emphasisPattern.exec(text)
        while match :
            whole  = match[0]
            pre    = match[1]
            marker = match[2]
            body   = match[3]
            post   = match[4]

          
            # parse links
            matchBegin = emphasisPattern.lastIndex - len(whole)
            beforeContent = text[previousLast : matchBegin + len(pre)]
            savedLastIndex = emphasisPattern.lastIndex
            result.append(self.parseLink(beforeContent))
            emphasisPattern.lastIndex = savedLastIndex

            bodyNode = [Node.createText(None, { value: body })]
            bodyContainer = self.emphasizeElementByMarker(bodyNode, marker)
            result.append(bodyContainer)

            previousLast = emphasisPattern.lastIndex - len(post)
            match = emphasisPattern.match(text)
        #end while

        if emphasisPattern.lastIndex == 0 or emphasisPattern.lastIndex != len(text) - 1:
            result.append(self.parseLink(text[previousLast:]))

        if len(result) == 1:
        # Avoid duplicated inline container wrapping
            return result[0]
        else:
            return Node.createInlineContainer(result)
  
    def parseLink(text):
        linkPattern = self.linkPattern
        linkPattern.lastIndex = 0

        match = []
        result = []
        previousLast = 0
        savedLastIndex = None

        match = linkPattern.exec(text)
        while match:
            whole = match[0]
            src   = match[1]
            title = match[2]

            #parse before content
            matchBegin = linkPattern.lastIndex - len(whole)
            beforeContent = text[previousLast : matchBegin]
            result.append(Node.createText(None, { value: beforeContent }))

            #parse link
            link = Node.createLink([])
            link.src = src
            if title:
                savedLastIndex = linkPattern.lastIndex
                link.appendChild(self.parseEmphasis(title))
                linkPattern.lastIndex = savedLastIndex
            else:
                link.appendChild(Node.createText(None, { value: src }))

            result.append(link)

            previousLast = linkPattern.lastIndex
            match = linkPattern.exec(text)
        #end while

        if linkPattern.lastIndex == 0 or linkPattern.lastIndex != len(text) - 1:
            result.append(Node.createText(None, { value: text[previousLast:] }))

        return Node.createInlineContainer(result)

    def emphasizeElementByMarker(element, marker):
        if marker == "*":
            return Node.createBold(element)
        elif marker == "/":
            return Node.createItalic(element)
        elif marker == "_":
            return Node.createUnderline(element)
        elif marker == "=" or marker == "~":
            return Node.createCode(element)
        elif marker == "+":
            return Node.createDashed(element)

    def buildEmphasisPattern(self):
        return "r'([" + self.preEmphasis + "]|^|\r?\n)"\
            "([" + self.markers + "])"\
            "([^" + self.borderForbidden + "]|"\
            "[^" + self.borderForbidden + "]"\
            + self.bodyRegexp + "[^" + self.borderForbidden + "])"\
            "\\2([" + self.postEmphasis +"]|$|\r?\n)'"             

       




def parseStream(stream, options):
    parser =  Parser()
    parser.initStatus(stream, options)
    parser.parseNodes()
    return parser.nodes



Parser.originalParseElement = Parser.parseElement