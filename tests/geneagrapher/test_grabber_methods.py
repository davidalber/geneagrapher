import os
import sys
from bs4 import BeautifulSoup
import unittest
from geneagrapher.grabber import *
from local_data_grabber import LocalDataGrabber


class TestGrabberMethods(unittest.TestCase):
    def data_file(self, filename):
        """Return the absolute path to the data file with given name."""
        return LocalDataGrabber.data_file(filename)

    def test_init(self):
        """Test constructor."""
        grabber = Grabber()
        self.assertIsInstance(grabber, Grabber)

    def test_get_record_bad(self):
        """Verify exception thrown from get_record() method for bad id."""
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
        grabber = Grabber()
        record = grabber.get_record(18231)
        self.assertEqual(len(record), 5)
        self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
        self.assertEqual(record['institution'], u"Universit\xe4t Helmstedt")
        self.assertEqual(record['year'], 1799)
        self.assertEqual(record['advisors'], set([18230]))
        self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                     151876, 29642, 18603,
                                                     19953, 217618, 62547,
                                                     225908, 166471, 18232,
                                                     18233, 234267, 165758]))

    def test_get_record_from_tree_bad(self):
        """Verify exception thrown from get_record_from_tree() method for bad
        id."""
        with open(self.data_file('999999999.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
        self.assertRaises(ValueError, get_record_from_tree, soup, 999999999)

        try:
            get_record_from_tree(soup, 999999999)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid id 999999999")
        else:
            self.fail()

    def test_get_record_from_tree_all_fields(self):
        """Test the get_record_from_tree() method for a record containing all
        fields."""
        with open(self.data_file('18231.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
        record = get_record_from_tree(soup, 18231)
        self.assertEqual(len(record), 5)
        self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
        self.assertEqual(record['institution'], u"Universit\xe4t Helmstedt")
        self.assertEqual(record['year'], 1799)
        self.assertEqual(record['advisors'], set([18230]))
        self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                     151876, 29642, 18603,
                                                     19953, 217618, 62547,
                                                     225908, 166471, 18232,
                                                     18233, 234267, 165758]))

        # Verify calling get_record_from_tree() twice does not have side
        # effect.
        record = get_record_from_tree(soup, 18231)
        self.assertEqual(len(record), 5)
        self.assertEqual(record['name'], u"Carl Friedrich Gau\xdf")
        self.assertEqual(record['institution'], u"Universit\xe4t Helmstedt")
        self.assertEqual(record['year'], 1799)
        self.assertEqual(record['advisors'], set([18230]))
        self.assertEqual(record['descendants'], set([234500, 234374, 55175,
                                                     151876, 29642, 18603,
                                                     19953, 217618, 62547,
                                                     225908, 166471, 18232,
                                                     18233, 234267, 165758]))

    def test_has_record_true(self):
        """Test the has_record() method with a tree containing a
        mathematician record."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertTrue(has_record(soup))

    def test_has_record_false(self):
        """Test the record_exists() method with a tree not containing a
        mathematician record."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertTrue(has_record(soup))

    def test_get_name(self):
        """Test the get_name() method."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(u"Valentin  Alberti", get_name(soup))

    def test_get_name_slash_l(self):
        """Test the get_name() method for a record containing a non-ASCII
        character."""
        with open(self.data_file('7383.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(u"W\u0142adys\u0142aw Hugo Dyonizy Steinhaus",
                             get_name(soup))

    def test_get_institution(self):
        """Test the get_institution() method for a record with an
        institution."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(u"Universit\xe4t Leipzig", get_institution(soup))

    def test_get_institution_no_institution(self):
        """Test the get_institution() method for a record with no
        institution."""
        with open(self.data_file('52965.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertIsNone(get_institution(soup))

    def test_get_year(self):
        """Test the get_year() method for a record with a graduation year."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_year(soup), 1678)

    def test_get_year_no_year(self):
        """Test the get_year() method for a record with no graduation year."""
        with open(self.data_file('53658.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertIsNone(get_year(soup))

    def test_get_advisors(self):
        """Test the get_advisors() method for a record with advisors."""
        with open(self.data_file('18231.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_advisors(soup), set([18230]))

    def test_get_advisors_multiple(self):
        """Test the get_advisors() method for a record with multiple
        advisors."""
        with open(self.data_file('19964.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_advisors(soup), set([17946, 47064]))

    def test_get_advisors_no_advisors(self):
        """Test the get_advisors() method for a record with no advisors."""
        with open(self.data_file('137717.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_advisors(soup), set([]))

    def test_get_descendants(self):
        """Test the get_descendants() method for a record with descendants."""
        expected_descendants = set([234500, 234374, 55175, 151876, 29642, 18603,
                                    19953, 217618, 62547, 225908, 166471, 18232,
                                    18233, 234267, 165758])
        with open(self.data_file('18231.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_descendants(soup), expected_descendants)

    def test_get_descendants_no_descendants(self):
        """Test the get_descendants() method for a record with no
        descendants."""
        with open(self.data_file('53658.html'), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
            self.assertEqual(get_descendants(soup), set([]))


if __name__ == '__main__':
    file_path = os.path.abspath(sys.argv[0])
    unittest.main()
else:
    file_path = os.path.abspath(sys.argv[0])
