from pstl.org.common.node import Node
import types
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class Exporter():
    exportOptions: {
        'headerOffset': 1,
        'exportFromLineNumber': False,
        'suppressSubScriptHandling': False,
        'suppressAutoLink': False,
        'suppressCheckboxHandling': False,
        # { "directive:": function (node, childText, auxData) {} }
        'customDirectiveHandler': None,
        # e.g., "org-js-"
        'htmlClassPrefix': None,
        'htmlIdPrefix': None
    }

    untitled: "Untitled"
    result: None
    # http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    urlPattern: "\b(?:https?:\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]) ig"
    imageExtensionPattern: "(" + "|".join(["bmp", "png", "jpeg", "jpg", "gif", "tiff","tif", "xbm", "xpm", "pbm", "pgm", "ppm", "svg"])+ ")$ i"
    def __init__(self, orgDocument, exportOptions = {}):
        self.output_ = StringIO()
        self.orgDocument = orgDocument
        self.documentOptions = orgDocument.options or {}
        self.exportOptions = exportOptions or {}

        self.headers = []
        self.headerOffset = hasattr(self.exportOptions, "headerOffset") and isinstance( self.exportOptions["headerOffset"], types.IntType) and self.exportOptions["headerOffset"] or 1
        self.sectionNumbers = [0]

    def export(self, filename=""):
        with open('output.tex','w') as f:
            f.write("Test")

    def createTocItem(headerNode, parentTocs):
        childTocs = []
        childTocs.parent = parentTocs
        tocItem = { 'headerNode': headerNode, 'childTocs': childTocs }
        return tocItem

    def convertNode(self, node, recordHeader, insideCodeElement):
        if not insideCodeElement:
            if node.type == Node.types['directive']:
                if node.directiveName == "example" or node.directiveName == "src":
                    insideCodeElement = True
            elif node.type == Node.types['preformatted']:
                insideCodeElement = True

        if isinstance(node, str):
            node = Node.createText(None, { value: node })


        childText = node.children and self.convertNodesInternal(node.children, recordHeader, insideCodeElement) or  ""

        auxData = self.computeAuxDataForNode(node)

        if node.type == Node.types['header']:
            # Parse task status
            taskStatus = None
            if childText.indexOf("TODO ") == 0:
                taskStatus = "todo";
            elif childText.indexOf("DONE ") == 0:
                taskStatus = "done"

            # Compute section number
            sectionNumberText = None
            if recordHeader:
                thisHeaderLevel = node.level
                previousHeaderLevel = len(self.sectionNumbers)
                if thisHeaderLevel > previousHeaderLevel:
                    # Fill missing section number
                    levelDiff = thisHeaderLevel - previousHeaderLevel
                    for x in range(0, levelDiff):
                        self.sectionNumbers[thisHeaderLevel - 1 - x] = 0 # Extend
                elif thisHeaderLevel < previousHeaderLevel:
                    self.sectionNumbers.length = thisHeaderLevel # Collapse

                self.sectionNumbers[thisHeaderLevel - 1] += 1
                sectionNumberText = self.sectionNumbers.join(".")
                node.sectionNumberText = sectionNumberText # Can be used in ToC

            text = self.convertHeader(node, childText, auxData, taskStatus, sectionNumberText);

            if recordHeader:
                self.headers.append(node)
        elif node.type == Node.types['orderedList']:
            text = self.convertOrderedList(node, childText, auxData)
        elif node.type == Node.types['unorderedList']:
            text = self.convertUnorderedList(node, childText, auxData)
        elif node.type == Node.types['definitionList']:
            text = self.convertDefinitionList(node, childText, auxData)
        elif node.type == Node.types['listElement']:
            if node.isDefinitionList:
                termText = self.convertNodesInternal(node.term, recordHeader, insideCodeElement)
                text = self.convertDefinitionItem(node, childText, auxData, termText, childText)
            else:
                text = self.convertListItem(node, childText, auxData)
        elif node.type == Node.types['paragraph']:
            text = self.convertParagraph(node, childText, auxData)
        elif node.type == Node.types['preformatted']:
            text = self.convertPreformatted(node, childText, auxData)
        elif node.type == Node.types['table']:
            text = self.convertTable(node, childText, auxData)
        elif node.type == Node.types['tableRow']:
            text = self.convertTableRow(node, childText, auxData)
        elif node.type == Node.types['tableCell']:
            if node.isHeader:
                text = self.convertTableHeader(node, childText, auxData)
            else:
                text = self.convertTableCell(node, childText, auxData)
        elif node.type == Node.types['horizontalRule']:
            text = self.convertHorizontalRule(node, childText, auxData)
        # ============================================================ //
        # Inline
        # ============================================================ //
        elif node.type == Node.types['inlineContainer']:
            text = self.convertInlineContainer(node, childText, auxData)
        elif node.type == Node.types['bold']:
            text = self.convertBold(node, childText, auxData)
        elif node.type == Node.types['italic']:
            text = self.convertItalic(node, childText, auxData)
        elif node.type == Node.types['underline']:
            text = self.convertUnderline(node, childText, auxData)
        elif node.type == Node.types['code']:
            text = self.convertCode(node, childText, auxData)
        elif node.type == Node.types['dashed']:
            text = self.convertDashed(node, childText, auxData)
        elif node.type == Node.types['link']:
            text = self.convertLink(node, childText, auxData)
        elif node.type == Node.types['directive']:
            if node.directiveName == "quote":
                text = self.convertQuote(node, childText, auxData)
            elif node.directiveName == "example":
                text = self.convertExample(node, childText, auxData)
            elif node.directiveName == "src":
                text = self.convertSrc(node, childText, auxData)
            elif node.directiveName == "html":
                text = self.convertHTML(node, childText, auxData)
            else:
                if hasattr(self.exportOptions, "customDirectiveHandler") and self.exportOptions["customDirectiveHandler"] and self.exportOptions["customDirectiveHandler"][node.directiveName]:
                    text = self.exportOptions["customDirectiveHandler"][node.directiveName](node, childText, auxData)
                else:
                    text = childText
        elif node.type == Node.types['text']:
            text = self.convertText(node.value, insideCodeElement)
        else:
            print ("Unknown node type: " + node.type)

        if hasattr(self.postProcess, '__call__'):
            text = self.postProcess(node, text, insideCodeElement)
        
        return text

    def convertText(self, text, insideCodeElement):
        escapedText = self.escapeSpecialChars(text)

        if not self.exportOptions.suppressSubScriptHandling and not insideCodeElement:
            escapedText = self.makeSubscripts(escapedText, insideCodeElement)
        if not self.exportOptions.suppressAutoLink:
            escapedText = self.linkURL(escapedText)

        return escapedText

    # By default, ignore html
    def convertHTML(node, childText, auxData):
        return childText

    def convertNodesInternal(self, nodes, recordHeader, insideCodeElement):
        nodesTexts = []
        for i in range(0, len(nodes)):
            node = nodes[i]
            nodeText = self.convertNode(node, recordHeader, insideCodeElement)
            nodesTexts.append(nodeText)

        return self.combineNodesTexts(nodesTexts)

    def convertHeaderBlock(headerBlock, recordHeader):
        print ("convertHeaderBlock is not implemented")

    def convertHeaderTree(headerTree, recordHeader):
        return self.convertHeaderBlock(headerTree, recordHeader)

    def convertNodesToHeaderTree(nodes, nextBlockBegin, blockHeader):
        childBlocks = []
        childNodes = []

        if nextBlockBegin:
            nextBlockBegin = 0
        if blockHeader:
            blockHeader = None
        for i in range(nextBlockBegin, len(nodes)):
            node = nodes[i]

            isHeader = node.type == Node.types['header']

            if not isHeader:
                childNodes.append(node)
                i = i + 1
                continue

            # Header
            if blockHeader and node.level <= blockHeader.level:
                # Finish Block
                break
            else:
                # blockHeader.level < node.level
                # Begin child block
                childBlock = self.convertNodesToHeaderTree(nodes, i + 1, node)
                childBlocks.append(childBlock)
                i = childBlock.nextIndex

        # Finish block
        return {
            'header': blockHeader,
            'childNodes': childNodes,
            'nextIndex': i,
            'childBlocks': childBlocks
        }

    def _convert_nodes(self, nodes, recordHeader, insideCodeElement):
        return self.convertNodesInternal(nodes, recordHeader, insideCodeElement)

    def combineNodesTexts(nodesTexts):
        return "".join(nodesTexts)

    def getNodeTextContent(node):
        if node.type == Node.types['text']:
            return self.escapeSpecialChars(node.value)
        else:
            return node.children and ("").join(map(self.getNodeTextContent, node.children)) or ""

    # @Override
    def escapeSpecialChars(self, text, insideCodeElement = False):
        print ("Implement escapeSpecialChars")

    # @Override
    def linkURL(text):
        return re.sub(
           self.urlPattern, 
           lambda x: self.makeLink("http://" + x.group()) if x.group().index("://") < 0 else self.makeLink(x.group()), 
           text
       )
    
    def makeLink(url):
        print("Implement makeLink")

    def makeSubscripts(text):
        if self.documentOptions["^"] == "{}":
            return re.sub('\b([^_ \t]*)_{([^}]*)}g', self.makeSubscript, text)
        elif self.documentOptions["^"]:
            return re.sub('\b([^_ \t]*)_([^_]*)\b/g', self.makeSubscript, text)
        else:
            return text

    def makeSubscript(match, body, subscript):
        print ("Implement makeSubscript")

    def stripParametersFromURL(url):
        return re.sub('\?.*$', "", url)