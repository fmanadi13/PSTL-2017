import ast
from pstl.ast.Location import Location
class Node(object):
    def __init__(self, ctx, parent = None):
        self.location = Location(ctx)
        self.parent = parent
        self.children = []

    def appendChild(self, child):
        self.children.append(child)

    def appendChildren(self, children: list):
        self.children.append(children)


    def __eq__(self, other):
        return NotImplemented
    def latex(self):
        return None



class Point():
    def __init__(self, line = 0, column = 0):
        self.line = line
        self.column = column

    def __str__(self):
        return f"[Line {self.line} | Column {self.column}]"

class Position():
    def __init__(self, start:Point, end:Point):
        self.start = start
        self.end = end

