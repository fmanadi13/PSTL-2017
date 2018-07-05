from pylatex.base_classes import Command
from pylatex.lists import List

class Checkboxes(List):
    """A class that represents a description list."""

    def add_item(self, isChecked, s):
        """Add an item to the list.

        Args
        ----
        isChecked: boolean
            Description of the item.
        s: str or `~.LatexObject`
            The item itself.
        """
        if isChecked == True:
            self.append(Command('CorrectChoice'))
        else:
            self.append(Command('choice'))

        self.append(s)

