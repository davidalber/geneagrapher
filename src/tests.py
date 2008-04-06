import unittest
import GGraph

# Unit tests for GGraph.
class TestRecordMethods(unittest.TestCase):
    """
    Unit tests for the GGraph.Record class.
    """
    def test001_init(self):
        # Test the constructor.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertEqual(record.name, "Carl Friedrich Gauss")
        self.assertEqual(record.institution, "Universitaet Helmstedt")
        self.assertEqual(record.year, 1799)
        self.assertEqual(record.id, 18231)
        
    def test002_init_bad_name(self):
        # Test constructor with bad 'name' parameter.
        self.assertRaises(TypeError, GGraph.Record, 1, "Universitaet Helmstedt", 1799, 18231)
        
    def test003_init_bad_institution(self):
        # Test constructor with bad 'institution' parameter.
        self.assertRaises(TypeError, GGraph.Record, "Carl Friedrich Gauss", 1, 1799, 18231)
        
    def test004_init_bad_year(self):
        # Test constructor with bad 'year' parameter.
        self.assertRaises(TypeError, GGraph.Record, "Carl Friedrich Gauss",
                          "Universitaet Helmstedt", "1799", 18231)
        
    def test005_init_bad_id(self):
        # Test constructor with bad 'id' parameter.
        self.assertRaises(TypeError, GGraph.Record, "Carl Friedrich Gauss",
                          "Universitaet Helmstedt", 1799, "18231")
        
    def test006_cmp_equal(self):
        # Verify two 'equal' records are compared correctly.
        record1 = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record1 == record2)
        
    def test007_cmp_unequal(self):
        # Verify two 'unequal' records are compared correctly.
        record1 = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = GGraph.Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        self.assert_(record1 < record2)

    def test008_hasInstitution_yes(self):
        # Verify hasInstitution() method returns True when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record.hasInstitution())

    def test009_hasInstitution_yes(self):
        # Verify hasInstitution() method returns False when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "", 1799, 18231)
        self.assert_(not record.hasInstitution())

    def test010_hasYear_yes(self):
        # Verify hasYear() method returns True when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record.hasYear())

    def test011_hasYear_no(self):
        # Verify hasYear() method returns False when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", -1, 18231)
        self.assert_(not record.hasYear())

class TestNodeMethods(unittest.TestCase):
    """
    Unit tests for the GGraph.Node class.
    """
    def setUp(self):
        self.record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
    
    def test001_init(self):
        # Test the constructor.
        node = GGraph.Node(self.record, [])
        self.assertEquals(node.record, self.record)
        self.assertEquals(node.ancestors, [])
        
    def test002_init_bad_record(self):
        # Test the constructor for a case where the record passed is not a Record
        # object.
        self.assertRaises(TypeError, GGraph.Node, 1, [])
        
    def test003_init_bad_ancestor_list(self):
        # Test the constructor for a case where the ancestor list is not a list.
        self.assertRaises(TypeError, GGraph.Node, self.record, 1)
        
    def test004_str_full(self):
        # Test __str__() method for Node with complete record.
        node = GGraph.Node(self.record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\nUniversitaet Helmstedt (1799)"
        self.assertEquals(nodestr, nodestrexpt)

    def test005_str_no_year(self):
        # Test __str__() method for Node containing record without year.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", -1, 18231)
        node = GGraph.Node(record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\nUniversitaet Helmstedt"
        self.assertEquals(nodestr, nodestrexpt)

    def test006_str_no_inst(self):
        # Test __str__() method for Node containing record without institution.
        record = GGraph.Record("Carl Friedrich Gauss", "", 1799, 18231)
        node = GGraph.Node(record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\n(1799)"
        self.assertEquals(nodestr, nodestrexpt)

    def test007_str_no_inst_no_id(self):
        # Test __str__() method for Node containing record without institution
        # or year.
        record = GGraph.Record("Carl Friedrich Gauss", "", -1, 18231)
        node = GGraph.Node(record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss"
        self.assertEquals(nodestr, nodestrexpt)

    def test008_cmp_equal(self):
        # Test comparison method for Nodes with identical records.
        record2 = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        node1 = GGraph.Node(self.record, [])
        node2 = GGraph.Node(record2, [])
        self.assert_(node1 == node2)

    def test009_cmp_unequal(self):
        # Test comparison method for Nodes with different records.
        record2 = GGraph.Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        node1 = GGraph.Node(self.record, [])
        node2 = GGraph.Node(record2, [])
        self.assert_(node1 < node2)

    def test010_add_ancestor(self):
        # Test the addAncestor() method.
        node = GGraph.Node(self.record, [])
        node.addAncestor(5)
        self.assertEquals(node.ancestors, [5])

    def test011_add_ancestor_bad_type(self):
        # Test the addAncestor() method for a case where the parameter type is incorrect.
        node = GGraph.Node(self.record, [])
        self.assertRaises(TypeError, node.addAncestor, '5')
        
    def test012_get_id(self):
        node = GGraph.Node(self.record, [])
        self.assertEquals(node.id(), 18231)


if __name__ == '__main__':
    unittest.main()