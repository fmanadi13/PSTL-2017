import unittest
from pstl.org.common.node import Node

class Test_test_node(unittest.TestCase):
    def test_creation(self):
        n = Node.createHeader([], {})
        self.assertTrue(n.toString() == "<header>")

    def test_no_first_child(self):
        n = Node.createHeader([], {})
        self.assertTrue(n.firstChild() == None)

    def test_no_last_child(self):
        n = Node.createHeader([], {})
        self.assertTrue(n.lastChild() == None)

if __name__ == '__main__':
    unittest.main()
