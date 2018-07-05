from pstl.ast.Node import Node
class AQ_Comment(Node):
    def __init__(self, ctx, content = "", parent = None):
        super(AQ_Comment, self).__init__(ctx, parent)
        self.content = content

    def __repr__(self):
        return f"<comment>{self.content}</comment>"

    def __str__(self):
        return f"<comment>{self.content}</comment>"
    def latex(self):
        return None