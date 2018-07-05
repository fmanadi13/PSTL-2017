from pylatex.base_classes  import ContainerCommand

class ParBox(ContainerCommand):
    r"""Allows the creation of headers."""

    _latex_name = "parbox"

    def __init__(self, width=None, *, data=None):
        r"""
        Args
        ----
        position: str
            the headers position: L, C, R
        data: str or `~.LatexObject`
            The data to place inside the Head element
        """

        self.width = width

        super().__init__(data=data, arguments=width)


