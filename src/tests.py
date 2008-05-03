import sys
import unittest
import GGraph
import grab
import geneagrapher

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

    def test009_hasInstitution_no(self):
        # Verify hasInstitution() method returns False when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", None, 1799, 18231)
        self.assert_(not record.hasInstitution())

    def test010_hasYear_yes(self):
        # Verify hasYear() method returns True when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record.hasYear())

    def test011_hasYear_no(self):
        # Verify hasYear() method returns False when the conditions are right.
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", None, 18231)
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
        record = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", None, 18231)
        node = GGraph.Node(record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\nUniversitaet Helmstedt"
        self.assertEquals(nodestr, nodestrexpt)

    def test006_str_no_inst(self):
        # Test __str__() method for Node containing record without institution.
        record = GGraph.Record("Carl Friedrich Gauss", None, 1799, 18231)
        node = GGraph.Node(record, [])
        nodestr = node.__str__()
        nodestrexpt = "Carl Friedrich Gauss \\n(1799)"
        self.assertEquals(nodestr, nodestrexpt)

    def test007_str_no_inst_no_id(self):
        # Test __str__() method for Node containing record without institution
        # or year.
        record = GGraph.Record("Carl Friedrich Gauss", None, None, 18231)
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

class TestGraphMethods(unittest.TestCase):
    """
    Unit tests for the GGraph.Graph class.
    """
    def setUp(self):
        self.record1 = GGraph.Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.node1 = GGraph.Node(self.record1, [])
        self.graph1 = GGraph.Graph([self.node1])
    
    def test001_init_empty(self):
        # Test the constructor.
        graph = GGraph.Graph()
        self.assertEquals(graph.heads, None)
        
    def test002_init(self):
        # Test the constructor.
        self.assert_(self.graph1.heads == [self.node1])
        self.assertEquals(self.graph1.nodes.keys(), [18231])
        self.assertEquals(self.graph1.nodes[18231], self.node1)
        
    def test003_init_bad_heads(self):
        # Test the constructor when passed a bad type for the heads parameter.
        self.assertRaises(TypeError, GGraph.Graph, 3)
        
    def test004_has_node_true(self):
        # Test the hasNode() method for a True case.
        self.assertEquals(self.graph1.hasNode(18231), True)
        
    def test005_has_node_false(self):
        # Test the hasNode() method for a False case.
        self.assertEquals(self.graph1.hasNode(1), False)
        
    def test006_get_node(self):
        # Test the getNode() method.
        node = self.graph1.getNode(18231)
        self.assert_(node == self.node1)
        
    def test007_get_node_not_found(self):
        # Test the getNode() method for a case where the node does not exist.
        node = self.graph1.getNode(1)
        self.assertEquals(node, None)
        
    def test008_get_node_list(self):
        # Test the getNodeList() method.
        self.assertEquals(self.graph1.getNodeList(), [18231])
        
    def test008_get_node_list_empty(self):
        # Test the getNodeList() method for an empty graph.
        graph = GGraph.Graph()
        self.assertEquals(graph.getNodeList(), [])
        
    def test009_add_node(self):
        # Test the addNode() method.
        self.graph1.addNode("Leonhard Euler", "Universitaet Basel", 1726, 38586, [])
        self.assertEquals([38586, 18231], self.graph1.getNodeList())
        self.assertEquals(self.graph1.heads, [self.node1])

    def test010_add_second_node_head(self):
        # Test the addNode() method when adding a second node and
        # marking it as a head node.
        self.graph1.addNode("Leonhard Euler", "Universitaet Basel", 1726, 38586, [], True)
        self.assertEquals([38586, 18231], self.graph1.getNodeList())
        self.assertEquals(self.graph1.heads, [self.node1, self.graph1.getNode(38586)])

    def test011_add_node_head(self):
        # Test the addNode() method when no heads exist.
        graph = GGraph.Graph()
        self.assertEquals(graph.heads, None)
        graph.addNode("Leonhard Euler", "Universitaet Basel", 1726, 38586, [])
        self.assertEquals(graph.heads, [graph.getNode(38586)])

    def test012_add_node_already_present(self):
        self.graph1.addNode("Leonhard Euler", "Universitaet Basel", 1726, 38586, [])
        self.assertEquals([38586, 18231], self.graph1.getNodeList())
        self.assertRaises(GGraph.DuplicateNodeError, self.graph1.addNode, "Leonhard Euler", "Universitaet Basel", 1726, 38586, [])

    def test013_generate_dot_file(self):
        # Test the generateDotFile() method.
        dotfileexpt = """digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    18231 [label="Carl Friedrich Gauss \\nUniversitaet Helmstedt (1799)"];

}
"""    
        dotfile = self.graph1.generateDotFile()
        self.assertEquals(dotfile, dotfileexpt)
        
    def test014_generate_dot_file(self):
        # Test the generateDotFile() method.
        graph = GGraph.Graph()
        graph.addNode("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231, [18230])
        graph.addNode("Johann Friedrich Pfaff", "Georg-August-Universitaet Goettingen", 1786, 18230, [66476])
        graph.addNode("Abraham Gotthelf Kaestner", "Universitaet Leipzig", 1739, 66476, [57670])
        graph.addNode("Christian August Hausen", "Martin-Luther-Universitaet Halle-Wittenberg", 1713, 57670, [72669])
        graph.addNode("Johann Christoph Wichmannshausen", "Universitaet Leipzig", 1685, 72669, [21235])
        graph.addNode("Otto Mencke", "Universitaet Leipzig", 1665, 21235, [])
        
        dotfileexpt = """digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    18231 [label="Carl Friedrich Gauss \\nUniversitaet Helmstedt (1799)"];
    18230 [label="Johann Friedrich Pfaff \\nGeorg-August-Universitaet Goettingen (1786)"];
    66476 [label="Abraham Gotthelf Kaestner \\nUniversitaet Leipzig (1739)"];
    57670 [label="Christian August Hausen \\nMartin-Luther-Universitaet Halle-Wittenberg (1713)"];
    72669 [label="Johann Christoph Wichmannshausen \\nUniversitaet Leipzig (1685)"];
    21235 [label="Otto Mencke \\nUniversitaet Leipzig (1665)"];

    18230 -> 18231;
    66476 -> 18230;
    57670 -> 66476;
    72669 -> 57670;
    21235 -> 72669;
}
"""
        dotfile = graph.generateDotFile()
        self.assertEquals(dotfile, dotfileexpt)

class TestGrabberMethods(unittest.TestCase):
    """
    Unit tests for the grab.Grabber class.
    """
    def setUp(self):
        self.grabber = grab.Grabber(18231)
        
    def test001_init(self):
        # Test constructor.
        self.assertEquals(self.grabber.id, 18231)
        self.assertEquals(self.grabber.pagestr, None)
        self.assertEquals(self.grabber.name, None)
        self.assertEquals(self.grabber.institution, None)
        self.assertEquals(self.grabber.year, None)
        self.assertEquals(self.grabber.advisors, [])

    def test002_get_page(self):
        # Test getPage() method.
        self.grabber.getPage()
        self.assert_(self.grabber.pagestr is not None)
        self.assert_(u"<title>The Mathematics Genealogy Project - Carl Gau\xdf</title>" in self.grabber.pagestr)
        # Get page again and test for adverse affects.
        self.grabber.getPage()
        self.assert_(u"<title>The Mathematics Genealogy Project - Carl Gau\xdf</title>" in self.grabber.pagestr)

    def test003_extract_info_bad(self):
        # Verify exception thrown for bad id.
        grabber = grab.Grabber(999999999)
        self.assertRaises(ValueError, grabber.extractNodeInformation)
        
    def test004_extract_info_all_fields(self):
        # Test the extractNodeInformation() method for a record containing all fields.
        [name, institution, year, advisors] = self.grabber.extractNodeInformation()
        self.assertEquals(name, self.grabber.name)
        self.assertEquals(institution, self.grabber.institution)
        self.assertEquals(year, self.grabber.year)
        self.assertEquals(advisors, self.grabber.advisors)
        self.assertEquals(name, u"Carl Friedrich Gau\xdf")
        self.assertEquals(institution, u"Universit\xe4t Helmstedt")
        self.assertEquals(year, 1799)
        self.assertEquals(advisors, [18230])
        
        # Verify calling extractNodeInformation() twice does not have side effect.
        [name, institution, year, advisors] = self.grabber.extractNodeInformation()
        self.assertEquals(name, u"Carl Friedrich Gau\xdf")
        self.assertEquals(institution, u"Universit\xe4t Helmstedt")
        self.assertEquals(year, 1799)
        self.assertEquals(advisors, [18230])
        
    def test005_extract_info_no_advisor(self):
        # Test the extractNodeInformation() method for a record with no advisor.
        grabber = grab.Grabber(21235)
        [name, institution, year, advisors] = grabber.extractNodeInformation()
        self.assertEquals(name, u"Otto  Mencke")
        self.assertEquals(institution, u"Universit\xe4t Leipzig")
        self.assertEquals(year, 1665)
        self.assertEquals(advisors, [])
        
    def test006_extract_info_no_year(self):
        # Test the extractNodeInformation() method for a record with no year.
        grabber = grab.Grabber(53658)
        [name, institution, year, advisors] = grabber.extractNodeInformation()
        self.assertEquals(name, u"S.  Cingolani")
        self.assertEquals(institution, u"Universit\xe0 di Pisa")
        self.assertEquals(year, None)
        self.assertEquals(advisors, [51261])
        
    def test007_extract_info_no_inst(self):
        # Test the extractNodeInformation() method for a record with no institution.
        # This test is also missing additional information already tested.
        grabber = grab.Grabber(52965)
        [name, institution, year, advisors] = grabber.extractNodeInformation()
        self.assertEquals(name, u"Walter  Mayer")
        self.assertEquals(institution, None)
        self.assertEquals(year, None)
        self.assertEquals(advisors, [])

    # Tests for special (from my point of view) characters:
    def test008_slash_l(self):
        # Test the extractNodeInformation() method for a record
        # containing a slash l character. Example:
        # http://www.genealogy.math.ndsu.nodak.edu/id.php?id=7383.
        grabber = grab.Grabber(7383)
        [name, institution, year, advisors] = grabber.extractNodeInformation()
        self.assertEquals(name, u"W\u0142adys\u0142aw Hugo Dyonizy Steinhaus")
        self.assertEquals(institution, u"Georg-August-Universit\xe4t G\xf6ttingen")
        self.assertEquals(year, 1911)
        self.assertEquals(advisors, [7298])
        
class TestGeneagrapherMethods(unittest.TestCase):
    """
    Unit tests for the geneagrapher.Geneagrapher class.
    """
    def setUp(self):
        self.ggrapher = geneagrapher.Geneagrapher()
        
    def test001_init(self):
        # Test constructor.
        self.assertEquals(isinstance(self.ggrapher.graph, GGraph.Graph), True)
        self.assertEquals(self.ggrapher.leaf_ids, [])
        self.assertEquals(self.ggrapher.get_ancestors, True)
        self.assertEquals(self.ggrapher.get_descendents, False)
        self.assertEquals(self.ggrapher.write_filename, None)
        
    def test002_parse_empty(self):
        # Test parseInput() with no arguments.
        sys.argv = ['geneagrapher']
        self.assertRaises(SyntaxError, self.ggrapher.parseInput)
        
    def test003_parse_default(self):
        # Test parseInput() with no options.
        sys.argv = ['geneagrapher', '3']
        self.ggrapher.get_ancestors = False
        self.ggrapher.get_descendents = True
        self.ggrapher.write_filename = "filler"
        self.ggrapher.parseInput()
        self.assertEquals(self.ggrapher.get_ancestors, True)
        self.assertEquals(self.ggrapher.get_descendents, False)
        self.assertEquals(self.ggrapher.write_filename, None)
        self.assertEquals(self.ggrapher.leaf_ids, [3])

    def test004_parse_options(self):
        # Test parseInput() with options.
        sys.argv = ['geneagrapher', '--without-ancestors', '--with-descendents', '--file=filler', '3', '43']
        self.ggrapher.parseInput()
        self.assertEquals(self.ggrapher.get_ancestors, False)
        self.assertEquals(self.ggrapher.get_descendents, True)
        self.assertEquals(self.ggrapher.write_filename, "filler")
        self.assertEquals(self.ggrapher.leaf_ids, [3, 43])

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecordMethods))
    suite.addTest(unittest.makeSuite(TestNodeMethods))
    suite.addTest(unittest.makeSuite(TestGraphMethods))
    suite.addTest(unittest.makeSuite(TestGrabberMethods))
    suite.addTest(unittest.makeSuite(TestGeneagrapherMethods))
    unittest.TextTestRunner(verbosity=1).run(suite)
