import unittest
from geneagrapher.grabber import Grabber


class TestGrabberMethods(unittest.TestCase):
    """Unit tests for the Grabber class."""
    def setUp(self):
        self.grabber = Grabber(18231)

    def test001_init(self):
        """Test constructor."""
        self.assertEqual(self.grabber.id, 18231)
        self.assertEqual(self.grabber.name, None)
        self.assertEqual(self.grabber.institution, None)
        self.assertEqual(self.grabber.year, None)
        self.assertEqual(self.grabber.advisors, set([]))
        self.assertEqual(self.grabber.descendants, set([]))

    def test002_extract_info_bad(self):
        """Verify exception thrown for bad id."""
        grabber = Grabber(999999999)
        self.assertRaises(ValueError, grabber.extract_node_information)

        try:
            grabber.extract_node_information()
        except ValueError as e:
            self.assertEqual(str(e), "Invalid id 999999999")
        else:
            self.fail()

    def test003_extract_info_all_fields(self):
        """Test the extract_node_information() method for a record containing
        all fields."""
        [name, institution, year, advisors,
         descendents] = self.grabber.extract_node_information()
        self.assertEqual(name, self.grabber.name)
        self.assertEqual(institution, self.grabber.institution)
        self.assertEqual(year, self.grabber.year)
        self.assertEqual(advisors, self.grabber.advisors)
        self.assertEqual(name, u"Carl Friedrich Gau\xdf")
        self.assertEqual(institution, u"Universit\xe4t Helmstedt")
        self.assertEqual(year, 1799)
        self.assertEqual(advisors, set([18230]))
        self.assertEqual(descendents, set([18603, 18233, 62547, 29642, 55175,
                                           29458, 19953, 18232, 151876]))

        # Verify calling extract_node_information() twice does not have side
        # effect.
        [name, institution, year, advisors,
         descendents] = self.grabber.extract_node_information()
        self.assertEqual(name, u"Carl Friedrich Gau\xdf")
        self.assertEqual(institution, u"Universit\xe4t Helmstedt")
        self.assertEqual(year, 1799)
        self.assertEqual(advisors, set([18230]))
        self.assertEqual(descendents, set([18603, 18233, 62547, 29642, 55175,
                                           29458, 19953, 18232, 151876]))

    def test004_extract_info_no_advisor(self):
        """Test the extract_node_information() method for a record with no
        advisor."""
        grabber = Grabber(137717)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"Valentin  Alberti")
        self.assertEqual(institution, u"Universit\xe4t Leipzig")
        self.assertEqual(year, 1678)
        self.assertEqual(advisors, set([]))
        self.assertEqual(descendents, set([127946]))

    def test005_extract_info_no_descendants(self):
        """Test the extract_node_information() method for a record with no
        descendants."""
        # This is currently identical to the extract_info_no_year test.
        grabber = Grabber(53658)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"S.  Cingolani")
        self.assertEqual(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([51261]))
        self.assertEqual(descendents, set([]))

    def test006_extract_info_no_year(self):
        """
        Test the extract_node_information() method for a record with no year.
        """
        # This example also has no descendents.
        grabber = Grabber(53658)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"S.  Cingolani")
        self.assertEqual(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([51261]))
        self.assertEqual(descendents, set([]))

    def test007_extract_info_no_inst(self):
        """Test the extract_node_information() method for a record with no
        institution."""
        # This test is also missing additional information already tested.
        grabber = Grabber(52965)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"Walter  Mayer")
        self.assertEqual(institution, None)
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([]))
        self.assertEqual(descendents, set([52996]))

    # Tests for special (from my point of view) characters:
    def test008_slash_l(self):
        """Test the extract_node_information() method for a record
        # containing a slash l character. Example:
        # http://www.genealogy.math.ndsu.nodak.edu/id.php?id=7383."""
        grabber = Grabber(7383)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"W\u0142adys\u0142aw Hugo Dyonizy Steinhaus")
        self.assertEqual(institution,
                         u"Georg-August-Universit\xe4t G\xf6ttingen")
        self.assertEqual(year, 1911)
        self.assertEqual(advisors, set([7298]))
        self.assertEqual(descendents, set([12681, 28292, 10275, 79297,
                                           36991, 17851, 127470, 51907,
                                           15165, 89841, 84016]))

    def test009_multiple_advisors(self):
        """Test for multiple advisors."""
        grabber = Grabber(19964)
        [name, institution, year, advisors,
         descendents] = grabber.extract_node_information()
        self.assertEqual(name, u"Rudolf Otto Sigismund Lipschitz")
        self.assertEqual(institution, u"Universit\xe4t Berlin")
        self.assertEqual(year, 1853)
        self.assertEqual(advisors, set([17946, 47064]))

if __name__ == '__main__':
    unittest.main()
