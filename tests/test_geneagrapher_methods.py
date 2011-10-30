import sys
import unittest
from geneagrapher import geneagrapher
from geneagrapher.graph import Graph

class TestGeneagrapherMethods(unittest.TestCase):
    """
    Unit tests for the geneagrapher.Geneagrapher class.
    """
    def setUp(self):
        self.ggrapher = geneagrapher.Geneagrapher()
        
    def test001_init(self):
        # Test constructor.
        self.assertEquals(isinstance(self.ggrapher.graph, Graph), True)
        self.assertEquals(self.ggrapher.leaf_ids, [])
        self.assertEquals(self.ggrapher.get_ancestors, False)
        self.assertEquals(self.ggrapher.get_descendants, False)
        self.assertEquals(self.ggrapher.verbose, False)
        self.assertEquals(self.ggrapher.write_filename, None)
        
    def test002_parse_empty(self):
        # Test parse_input() with no arguments.
        sys.argv = ['geneagrapher']
        self.assertRaises(SyntaxError, self.ggrapher.parse_input)
        
    def test003_parse_default(self):
        # Test parse_input() with no options.
        sys.argv = ['geneagrapher', '3']
        self.ggrapher.get_ancestors = False
        self.ggrapher.get_descendents = True
        self.ggrapher.write_filename = "filler"
        self.ggrapher.parse_input()
        self.assertEquals(self.ggrapher.get_ancestors, False)
        self.assertEquals(self.ggrapher.get_descendants, False)
        self.assertEquals(self.ggrapher.verbose, False)
        self.assertEquals(self.ggrapher.write_filename, None)
        self.assertEquals(self.ggrapher.leaf_ids, [3])

    def test004_parse_options(self):
        # Test parse_input() with options.
        sys.argv = ['geneagrapher', '--with-ancestors', '--with-descendants', '--file=filler', '--verbose', '3', '43']
        self.ggrapher.parse_input()
        self.assertEquals(self.ggrapher.get_ancestors, True)
        self.assertEquals(self.ggrapher.get_descendants, True)
        self.assertEquals(self.ggrapher.verbose, True)
        self.assertEquals(self.ggrapher.write_filename, "filler")
        self.assertEquals(self.ggrapher.leaf_ids, [3, 43])

if __name__ == '__main__':
    unittest.main()
