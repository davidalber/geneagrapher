import unittest
from geneagrapher.graph import Node, Record

class TestNodeMethods(unittest.TestCase):
    """
    Unit tests for the Node class.
    """
    def setUp(self):
        self.record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
    
    def test001_init(self):
        # Test the constructor.
        node = Node(self.record, [], [])
        self.assertEquals(node.record, self.record)
        self.assertEquals(node.ancestors, [])
        self.assertEquals(node.descendants, [])
        
    def test002_init_bad_record(self):
        # Test the constructor for a case where the record passed is not a Record
        # object.
        self.assertRaises(TypeError, Node, 1, [], [])
        
    def test003_init_bad_ancestor_list(self):
        # Test the constructor for a case where the ancestor list is not a list.
        self.assertRaises(TypeError, Node, self.record, 1, [])

    def test003_2_init_bad_descendent_list(self):
        # Test the constructor for a case where the descendent list is not a list.
        self.assertRaises(TypeError, Node, self.record, [], 1)
        
    def test004_str_full(self):
        # Test __str__() method for Node with complete record.
        node = Node(self.record, [], [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\nUniversitaet Helmstedt (1799)"
        self.assertEquals(nodestr, nodestrexpt)

    def test005_str_no_year(self):
        # Test __str__() method for Node containing record without year.
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", None, 18231)
        node = Node(record, [], [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\nUniversitaet Helmstedt"
        self.assertEquals(nodestr, nodestrexpt)

    def test006_str_no_inst(self):
        # Test __str__() method for Node containing record without institution.
        record = Record("Carl Friedrich Gauss", None, 1799, 18231)
        node = Node(record, [], [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\n(1799)"
        self.assertEquals(nodestr, nodestrexpt)

    def test007_str_no_inst_no_id(self):
        # Test __str__() method for Node containing record without institution
        # or year.
        record = Record("Carl Friedrich Gauss", None, None, 18231)
        node = Node(record, [], [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss"
        self.assertEquals(nodestr, nodestrexpt)

    def test008_cmp_equal(self):
        # Test comparison method for Nodes with identical records.
        record2 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        node1 = Node(self.record, [], [])
        node2 = Node(record2, [], [])
        self.assert_(node1 == node2)

    def test009_cmp_unequal(self):
        # Test comparison method for Nodes with different records.
        record2 = Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        node1 = Node(self.record, [], [])
        node2 = Node(record2, [], [])
        self.assert_(node1 < node2)

    def test010_add_ancestor(self):
        # Test the add_ancestor() method.
        node = Node(self.record, [], [])
        node.add_ancestor(5)
        self.assertEquals(node.ancestors, [5])

    def test011_add_ancestor_bad_type(self):
        # Test the add_ancestor() method for a case where the parameter type is incorrect.
        node = Node(self.record, [], [])
        self.assertRaises(TypeError, node.add_ancestor, '5')
        
    def test012_get_id(self):
        node = Node(self.record, [], [])
        self.assertEquals(node.get_id(), 18231)

    def test013_set_id(self):
        # Test the set_id() method.
        node = Node(self.record, [], [])
        self.assertEquals(node.get_id(), 18231)
        node.set_id(15)
        self.assertEquals(node.get_id(), 15)

if __name__ == '__main__':
    unittest.main()
