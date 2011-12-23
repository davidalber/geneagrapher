import unittest
from geneagrapher.grabber import Grabber


class TestGrabberMethods(unittest.TestCase):
    """Unit tests for the Grabber class."""
    def setUp(self):
        self.grabber = Grabber()

    def test_init(self):
        """Test constructor."""
        self.assertIsInstance(self.grabber, Grabber)

    def test_get_record_bad(self):
        """Verify exception thrown for bad id."""
        grabber = Grabber()
        self.assertRaises(ValueError, grabber.get_record, 999999999)

        try:
            grabber.get_record(999999999)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid id 999999999")
        else:
            self.fail()

    def test_get_record_all_fields(self):
        """Test the get_record() method for a record containing all fields."""
        [name, institution, year, advisors,
         descendents] = self.grabber.get_record(18231)
        self.assertEqual(name, u"Carl Friedrich Gau\xdf")
        self.assertEqual(institution, u"Universit\xe4t Helmstedt")
        self.assertEqual(year, 1799)
        self.assertEqual(advisors, set([18230]))
        self.assertEqual(descendents, set([18603, 18233, 62547, 29642, 55175,
                                           29458, 19953, 18232, 151876]))

        # Verify calling get_record() twice does not have side effect.
        [name, institution, year, advisors,
         descendents] = self.grabber.get_record(18231)
        self.assertEqual(name, u"Carl Friedrich Gau\xdf")
        self.assertEqual(institution, u"Universit\xe4t Helmstedt")
        self.assertEqual(year, 1799)
        self.assertEqual(advisors, set([18230]))
        self.assertEqual(descendents, set([18603, 18233, 62547, 29642, 55175,
                                           29458, 19953, 18232, 151876]))

    def test_get_record_no_advisor(self):
        """Test the get_record() method for a record with no advisor."""
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(137717)
        self.assertEqual(name, u"Valentin  Alberti")
        self.assertEqual(institution, u"Universit\xe4t Leipzig")
        self.assertEqual(year, 1678)
        self.assertEqual(advisors, set([]))
        self.assertEqual(descendents, set([127946]))

    def test_get_record_no_descendants(self):
        """Test the get_record() method for a record with no descendants."""
        # This is currently identical to the get_record_no_year test.
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(53658)
        self.assertEqual(name, u"S.  Cingolani")
        self.assertEqual(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([51261]))
        self.assertEqual(descendents, set([]))

    def test_get_record_no_year(self):
        """Test the get_record() method for a record with no year."""
        # This example also has no descendents.
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(53658)
        self.assertEqual(name, u"S.  Cingolani")
        self.assertEqual(institution, u"Scuola Normale Superiore di Pisa")
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([51261]))
        self.assertEqual(descendents, set([]))

    def test_get_record_no_inst(self):
        """Test the get_record() method for a record with no institution."""
        # This test is also missing additional information already tested.
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(52965)
        self.assertEqual(name, u"Walter  Mayer")
        self.assertEqual(institution, None)
        self.assertEqual(year, None)
        self.assertEqual(advisors, set([]))
        self.assertEqual(descendents, set([52996]))

    # Tests for special (from my point of view) characters:
    def test_slash_l(self):
        """Test the get_record() method for a record containing a slash l
        character. Example:
        http://www.genealogy.math.ndsu.nodak.edu/id.php?id=7383."""
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(7383)
        self.assertEqual(name, u"W\u0142adys\u0142aw Hugo Dyonizy Steinhaus")
        self.assertEqual(institution,
                         u"Georg-August-Universit\xe4t G\xf6ttingen")
        self.assertEqual(year, 1911)
        self.assertEqual(advisors, set([7298]))
        self.assertEqual(descendents, set([12681, 28292, 10275, 79297,
                                           36991, 17851, 127470, 51907,
                                           15165, 89841, 84016]))

    def test_multiple_advisors(self):
        """Test for multiple advisors."""
        grabber = Grabber()
        [name, institution, year, advisors,
         descendents] = grabber.get_record(19964)
        self.assertEqual(name, u"Rudolf Otto Sigismund Lipschitz")
        self.assertEqual(institution, u"Universit\xe4t Berlin")
        self.assertEqual(year, 1853)
        self.assertEqual(advisors, set([17946, 47064]))

if __name__ == '__main__':
    unittest.main()
