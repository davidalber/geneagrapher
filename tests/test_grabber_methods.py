import unittest
from geneagrapher.grabber import Grabber

class TestGrabberMethods(unittest.TestCase):
    """
    Unit tests for the Grabber class.
    """
    def setUp(self):
        self.grabber = Grabber(18231)
        
    def test001_init(self):
        # Test constructor.
        self.assertEquals(self.grabber.id, 18231)
        self.assertEquals(self.grabber.name, None)
        self.assertEquals(self.grabber.institution, None)
        self.assertEquals(self.grabber.year, None)
        self.assertEquals(self.grabber.advisors, [])
        self.assertEquals(self.grabber.descendants, [])

    def test002_extract_info_bad(self):
        # Verify exception thrown for bad id.
        grabber = Grabber(999999999)
        self.assertRaises(ValueError, grabber.extract_node_information)
        
    def test003_extract_info_all_fields(self):
        # Test the extract_node_information() method for a record containing all fields.
        [name, institution, year, advisors, descendents] = self.grabber.extract_node_information()
        self.assertEquals(name, self.grabber.name)
        self.assertEquals(institution, self.grabber.institution)
        self.assertEquals(year, self.grabber.year)
        self.assertEquals(advisors, self.grabber.advisors)
        self.assertEquals(name, u"Carl Friedrich Gau\xdf")
        self.assertEquals(institution, u"Universit\xe4t Helmstedt")
        self.assertEquals(year, 1799)
        self.assertEquals(advisors, [18230])
        self.assertEquals(descendents, [18603, 18233, 62547, 29642, 55175, 29458, 19953, 18232, 151876])
        
        # Verify calling extract_node_information() twice does not have side effect.
        [name, institution, year, advisors, descendents] = self.grabber.extract_node_information()
        self.assertEquals(name, u"Carl Friedrich Gau\xdf")
        self.assertEquals(institution, u"Universit\xe4t Helmstedt")
        self.assertEquals(year, 1799)
        self.assertEquals(advisors, [18230])
        self.assertEquals(descendents, [18603, 18233, 62547, 29642, 55175, 29458, 19953, 18232, 151876])
        
    def test004_extract_info_no_advisor(self):
        # Test the extract_node_information() method for a record with no advisor.
        grabber = Grabber(137717)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"Valentin  Alberti")
        self.assertEquals(institution, u"Universit\xe4t Leipzig")
        self.assertEquals(year, 1678)
        self.assertEquals(advisors, [])
        self.assertEquals(descendents, [127946])
        
    def test005_extract_info_no_descendants(self):
        # Test the extract_node_information() method for a record with no
        # descendants.

        # This is currently identical to the extract_info_no_year test.
        grabber = Grabber(53658)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"S.  Cingolani")
        self.assertEquals(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEquals(year, None)
        self.assertEquals(advisors, [51261])
        self.assertEquals(descendents, [])

    def test006_extract_info_no_year(self):
        # Test the extract_node_information() method for a record with no year.
        # This example also has no descendents.
        grabber = Grabber(53658)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"S.  Cingolani")
        self.assertEquals(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEquals(year, None)
        self.assertEquals(advisors, [51261])
        self.assertEquals(descendents, [])
        
    def test007_extract_info_no_inst(self):
        # Test the extract_node_information() method for a record with no institution.
        # This test is also missing additional information already tested.
        grabber = Grabber(52965)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"Walter  Mayer")
        self.assertEquals(institution, None)
        self.assertEquals(year, None)
        self.assertEquals(advisors, [])
        self.assertEquals(descendents, [52996])

    # Tests for special (from my point of view) characters:
    def test008_slash_l(self):
        # Test the extract_node_information() method for a record
        # containing a slash l character. Example:
        # http://www.genealogy.math.ndsu.nodak.edu/id.php?id=7383.
        grabber = Grabber(7383)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"W\u0142adys\u0142aw Hugo Dyonizy Steinhaus")
        self.assertEquals(institution, u"Georg-August-Universit\xe4t G\xf6ttingen")
        self.assertEquals(year, 1911)
        self.assertEquals(advisors, [7298])

    def test009_multiple_advisors(self):
        # Test for multiple advisors.
        grabber = Grabber(19964)
        [name, institution, year, advisors, descendents] = grabber.extract_node_information()
        self.assertEquals(name, u"Rudolf Otto Sigismund Lipschitz")
        self.assertEquals(institution, u"Universit\xe4t Berlin")
        self.assertEquals(year, 1853)
        self.assertEquals(advisors, [17946, 47064])

if __name__ == '__main__':
    unittest.main()
