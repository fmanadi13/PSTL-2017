from functools import reduce
from pstl.org.utils.helper import Helper

class Node():
    """Base class for Lists"""
    types ={}
    def __init__(self, type, children = []):
        self.type = type
        self.children = []
        self.previousSibling = None
        self.parent = None
        if children:
            [self.appendChild(ch) for ch in children]

    def firstChild(self):
        if len(self.children) < 1:
            return None
        else:
            return self.children[0]

    def lastChild(self):
        if len(self.children) < 1:
            return None
        else:
            return self.children[len(self.children) - 1]
    
    def appendChild(self, newChild): 
        self.previousSibling = len(self.children) < 1 and None or self.lastChild()
        self.children.append(newChild)
        newChild.previousSibling = self.previousSibling
        newChild.parent = self

    def __str__(self):
        string = "<" + self.type + ">"
        if hasattr(self, 'value'):
            string += " " + self.value
        elif self.children:
            temp = []
            for i, node in enumerate(self.children):
                temp.append("#" + str(i) + " " + node.__str__())
            string += reduce((lambda ls, line: ls + "\n" + line), temp)

        return string

    def define(name, postProcess = None):
        Node.types[name] = name
        methodName = "create" + Helper._upper_first_letter(name)
        postProcessGiven = hasattr(postProcess, '__call__')
        Helper._bind_method(Node, lambda children, options = {}: postProcessGiven and postProcess(Node(name, children), options or {}) or Node(name, children), methodName)
                




Node.define("text", (lambda n, options:Helper._merge_cls_attrs(n, options)))
Node.define("header", (lambda n, options: Helper._merge_cls_attrs(n, options)))
Node.define("orderedList")
Node.define("unorderedList")
Node.define("definitionList")
Node.define("checkboxList")
Node.define("listElement")
Node.define("paragraph")
Node.define("preformatted")
Node.define("table")
Node.define("tableRow")
Node.define("tableCell", (lambda n, options:Helper._merge_cls_attrs(n, options)))
Node.define("horizontalRule")
Node.define("directive")
Node.define("option", (lambda n, options: Helper._merge_cls_attrs(n, options)))
# Inline
Node.define("inlineContainer")

Node.define("bold")
Node.define("italic")
Node.define("underline")
Node.define("code")
Node.define("verbatim")
Node.define("dashed")
Node.define("link", (lambda n, options:Helper._merge_cls_attrs(n, options)))

