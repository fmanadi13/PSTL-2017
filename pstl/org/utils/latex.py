import re
import types
from pstl.org.utils.export import Exporter
from pstl.org.common.node import Node

class Latex(Exporter):
    replaceRegexp: None
    def __init__(self, orgDocument, options):
        Exporter.__init__(self, orgDocument, options)
        self.output = self.export()
    def export(self):
        self._convert_nodes(self.orgDocument.nodes, False, False)
        title = self.orgDocument.title and self.convertNode(self.orgDocument.title) or self.untitled
        titleHTML = self.tag("h" + Math.max(Number(self.headerOffset), 1), title)
        contentHTML = self.convertNodes(self.orgDocument.nodes, True)
        toc = self.computeToc(self.documentOptions["toc"])
        tocHTML = self.tocToHTML(toc)

        return {
            'title': title,
            'titleHTML': titleHTML,
            'contentHTML': contentHTML,
            'tocHTML': tocHTML,
            'toc': toc,
            toString: lambda : titleHTML + tocHTML + "\n" + contentHTML
        }

    def computeAuxDataForNode(self, node):
        while node.parent and node.parent.type == Node.types['inlineContainer']:
            node = node.parent
        attributesNode = node.previousSibling
        attributesText = ""
        while attributesNode and attributesNode.type == Node.types['directive'] and attributesNode.directiveName == "attr_html:":
            attributesText += attributesNode.directiveRawValue + " "
            attributesNode = attributesNode.previousSibling
        return attributesText

    
    # Method to construct org-js generated class
    def orgClassName(className):
        return self.exportOptions.htmlClassPrefix and self.exportOptions.htmlClassPrefix + className or className

    # Method to construct org-js generated id
    def orgId(id):
        return self.exportOptions.htmlIdPrefix and self.exportOptions.htmlIdPrefix + id or id



    # ----------------------------------------------------
    #  Node conversion
    #   ----------------------------------------------------
    def convertHeader(node, childText, auxData, taskStatus, sectionNumberText):
        headerAttributes = {}

        if taskStatus:
            childText = self.inlineTag("span", childText[0: 4], {"class": "task-status " + taskStatus}) + childText[5:]

        if sectionNumberText:
            childText = self.inlineTag("span", sectionNumberText, {"class": "section-number"}) + childText
            headerAttributes["id"] = "header-" + sectionNumberText.replace('\.g', "-")
        
        if taskStatus:
            headerAttributes["class"] = "task-status " + taskStatus

        return self.tag("h" + (self.headerOffset + node.level), childText, headerAttributes, auxData)

    def convertOrderedList(node, childText, auxData):
        return self.tag("ol", childText, None, auxData)

    def convertUnorderedList(node, childText, auxData):
        return self.tag("ul", childText, None, auxData)

    def convertDefinitionList(node, childText, auxData):
        return self.tag("dl", childText, None, auxData)

    def convertDefinitionItem(node, childText, auxData, term, definition):
        return self.tag("dt", term) + self.tag("dd", definition)

    def convertListItem(node, childText, auxData):
        if (self.exportOptions.suppressCheckboxHandling):
            return self.tag("li", childText, None, auxData)
        else:
            listItemAttributes = {}
            listItemText = childText
            # Embed checkbox
            m = '^\s*\[(?P<checked>X| |-)\](?P<content>[\s\S]*)'.search(listItemText)
            if m:
                listItemText = m.group('content')
                checkboxIndicator = m.group('checked')

                checkboxAttributes = { type: "checkbox" }
                if checkboxIndicator == "X":
                    checkboxAttributes["checked"] = "True"
                    listItemAttributes["data-checkbox-status"] = "done"
                elif checkboxIndicator == "-":
                    listItemAttributes["data-checkbox-status"] = "intermediate"
                else:
                    listItemAttributes["data-checkbox-status"] = "undone"

                listItemText = self.inlineTag("input", None, checkboxAttributes) + listItemText

            return self.tag("li", listItemText, listItemAttributes, auxData)

    def convertParagraph(node, childText, auxData):
        return self.tag("p", childText, None, auxData)

    def convertPreformatted(node, childText, auxData):
        return self.tag("pre", childText, None, auxData)

    def convertTable(node, childText, auxData):
        return self.tag("table", self.tag("tbody", childText), None, auxData)

    def convertTableRow(node, childText, auxData):
        return self.tag("tr", childText)

    def convertTableHeader(node, childText, auxData):
        return self.tag("th", childText)

    def convertTableCell(node, childText, auxData):
        return self.tag("td", childText)

    def convertHorizontalRule(node, childText, auxData):
        return self.tag("hr", None, None, auxData)

    def convertInlineContainer(node, childText, auxData):
        return childText

    def convertBold(node, childText, auxData):
        return self.inlineTag("textbf", childText)

    def convertItalic(node, childText, auxData):
        return self.inlineTag("textit", childText)

    def convertUnderline(node, childText, auxData):
        return self.inlineTag("underline", childText)

    def convertCode(node, childText, auxData):
        return self.inlineTag("code", childText)

    def convertDashed(node, childText, auxData):
        return self.inlineTag("sout", childText)

    def convertLink(node, childText, auxData):
        srcParameterStripped = self.stripParametersFromURL(node.src)
        if self.imageExtensionPattern.exec(srcParameterStripped):
            imgText = self.getNodeTextContent(node)
            return self.inlineTag("img", None, {
                'src': node.src,
                'alt': imgText,
                'title': imgText
            }, auxData)
        else:
          return self.inlineTag("a", childText, { 'href': node.src })

    def convertQuote(node, childText, auxData):
        return self.tag("blockquote", childText, None, auxData)

    def convertExample(node, childText, auxData):
        return self.tag("pre", childText, None, auxData)

    def convertSrc(node, childText, auxData):
        codeLanguage = len(node.directiveArguments) and node.directiveArguments[0] or "unknown"
        childText = self.tag("code", childText, {
            "class": "language-" + codeLanguage
        }, auxData)
        return self.tag("pre", childText, {"class": "prettyprint"})

    # @override
    def convertHTML(node, childText, auxData):
        if node.directiveName == "html:":
            return node.directiveRawValue
        elif node.directiveName == "html":
            return "\n".join(map((lambda textNode: textNode.value) , node.children))
        else:
          return childText

    # @implement
    def convertHeaderBlock(headerBlock, level, index):
        level = level or 0
        index = index or 0

        contents = []

        headerNode = headerBlock.header
        if headerNode:
            contents.append(self.convertNode(headerNode))

        blockContent = self.convertNodes(headerBlock.childNodes)
        contents.append(blockContent)

        childBlockContent = "\n".join(map((lambda block, idx:self.convertHeaderBlock(block, level + 1, idx)), headerBlock.childBlocks))
        contents.append(childBlockContent)

        contentsText = "\n".join(contents)

        if headerNode:
            return self.tag("section", "\n" + "\n".join(contents), {"class": "block block-level-" + level})
        else:
            return contentsText

    # ----------------------------------------------------
    #  Supplemental methods
    #   ----------------------------------------------------

    replaceMap: {
    # [replacing pattern, predicate]
        "&": ["&#38;", None],
        "<": ["&#60;", None],
        ">": ["&#62;", None],
        '"': ["&#34;", None],
        "'": ["&#39;", None],
        "->": ["&#10132;", lambda text, insideCodeElement: self.exportOptions.translateSymbolArrow and not insideCodeElement]
    }

    

    # @implement @override
    def escapeSpecialChars(text, insideCodeElement):
        if not Latex.replaceRegexp:
            Latex.replaceRegexp = re.compile("|".join(replaceMap.keys()))

        replaceMap = self.replaceMap
        #return text.replace(self.replaceRegexp, function (matched) {
        #    if not replaceMap[matched]:
        #        raise Exception("escapeSpecialChars: Invalid match")

        #    predicate = replaceMap[matched][1]
        #    if hasattr(predicate, "call") and not predicate.call(self, text, insideCodeElement):
                # Not fullfill the predicate
        #        return matched

        #    return replaceMap[matched][0]
        #})

    # @implement
    def postProcess(self, node, currentText, insideCodeElement):
        if hasattr(self.exportOptions, "exportFromLineNumber") and self.exportOptions["exportFromLineNumber"] and isinstance(node.fromLineNumber, types.IntType):
            # Wrap with line number information
            currentText = self.inlineTag("div", currentText, {"data-line-number": node.fromLineNumber})
        return currentText

    # @implement
    def makeLink(url):
        return "<a href=\"" + url + "\">" + decodeURIComponent(url) + "</a>"

    # @implement
    def makeSubscript(match, body, subscript):
        return "<span class=\"org-subscript-parent\">" + body + "</span><span class=\"org-subscript-child\">" + subscript + "</span>"

    # ----------------------------------------------------
    #  Specific methods
    #   ----------------------------------------------------

    def attributesObjectToString(attributesObject):
        attributesString = ""
        for attributeName in attributesObject:
            if hasattr(attributeName, attributesObject):
                attributeValue = attributesObject[attributeName]
                # To avoid id/class name conflicts with other frameworks,
                # users can add arbitrary prefix to org-js generated
                # ids/classes via exportOptions.
                if attributeName == "class":
                    attributeValue = self.orgClassName(attributeValue)
                elif attributeName == "id":
                    attributeValue = self.orgId(attributeValue)
                attributesString += " " + attributeName + "=\"" + attributeValue + "\""

        return attributesString

    def inlineTag(name, innerText, attributesObject, auxAttributesText):
        attributesObject = attributesObject or {}

        ltxString = '\\' + name 
        ltxString = ltxString + "{\n"
        # TODO: check duplicated attributes
        #if auxAttributesText:
        #    htmlString += " " + auxAttributesText
        #htmlString += self.attributesObjectToString(attributesObject)

        ltxString += innerText + "\n}"

        return htmlString

    def tag(name, innerText, attributesObject, auxAttributesText):
        return self.inlineTag(name, innerText, attributesObject, auxAttributesText) + "\n"
