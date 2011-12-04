import unittest
from geneagrapher.graph import Node, Record


class TestNodeMethods(unittest.TestCase):
    """Unit tests for the Node class."""
    def setUp(self):
        self.record = Record(u"Carl Friedrich Gau\xdf",
                             u"Universit\xe4t Helmstedt", 1799, 18231)

    def test_init(self):
        """Test the constructor."""
        node = Node(self.record, set(), set())
        self.assertEqual(node.record, self.record)
        self.assertEqual(node.ancestors, set())
        self.assertEqual(node.descendants, set())

    def test_init_bad_record(self):
        """Test the constructor for a case where the record passed is not a
        Record object."""
        self.assertRaises(TypeError, Node, 1, set(), set())

    def test_init_bad_ancestor_list(self):
        """Test the constructor for a case where the ancestor list is not a
        list."""
        self.assertRaises(TypeError, Node, self.record, 1, set())

    def test_2_init_bad_descendent_list(self):
        """Test the constructor for a case where the descendent list is not a
        list."""
        self.assertRaises(TypeError, Node, self.record, set(), 1)

    def test_unicode_full(self):
        """Test __unicode__() method for Node with complete record."""
        node = Node(self.record, set(), set())
        nodestr = node.__unicode__()
        nodestrexpt = u"Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt \
(1799)"
        self.assertEqual(nodestr, nodestrexpt)

    def test_unicode_no_year(self):
        """
        Test __unicode__() method for Node containing record without year.
        """
        record = Record(self.record.name, self.record.institution, None, 18231)
        node = Node(record, set(), set())
        nodestr = node.__unicode__()
        nodestrexpt = u"Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt"
        self.assertEqual(nodestr, nodestrexpt)

    def test_unicode_no_inst(self):
        """Test __unicode__() method for Node containing record without
        institution."""
        record = Record(self.record.name, None, 1799, 18231)
        node = Node(record, set(), set())
        nodestr = node.__unicode__()
        nodestrexpt = u"Carl Friedrich Gau\xdf \\n(1799)"
        self.assertEqual(nodestr, nodestrexpt)

    def test_unicode_no_inst_no_id(self):
        """Test __unicode__() method for Node containing record without
        institution or year."""
        record = Record(self.record.name, None, None, 18231)
        node = Node(record, set(), set())
        nodestr = node.__unicode__()
        nodestrexpt = u"Carl Friedrich Gau\xdf"
        self.assertEqual(nodestr, nodestrexpt)

    def test_cmp_equal(self):
        """Test comparison method for Nodes with identical records."""
        record2 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt",
                         1799, 18231)
        node1 = Node(self.record, set(), set())
        node2 = Node(record2, set(), set())
        self.assert_(node1 == node2)

    def test_cmp_unequal(self):
        """Test comparison method for Nodes with different records."""
        record2 = Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        node1 = Node(self.record, set(), set())
        node2 = Node(record2, set(), set())
        self.assert_(node1 < node2)

    def test_add_ancestor(self):
        """Test the add_ancestor() method."""
        node = Node(self.record, set(), set())
        node.add_ancestor(5)
        self.assertEqual(node.ancestors, set([5]))

    def test_add_ancestor_bad_type(self):
        """Test the add_ancestor() method for a case where the parameter type
        is incorrect."""
        node = Node(self.record, set(), set())
        self.assertRaises(TypeError, node.add_ancestor, '5')

    def test_get_id(self):
        """Test the get_id() method."""
        node = Node(self.record, set(), set())
        self.assertEqual(node.get_id(), 18231)

    def test_set_id(self):
        """Test the set_id() method."""
        node = Node(self.record, set(), set())
        self.assertEqual(node.get_id(), 18231)
        node.set_id(15)
        self.assertEqual(node.get_id(), 15)

if __name__ == '__main__':
    unittest.main()
