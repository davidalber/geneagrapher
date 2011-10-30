import unittest
from geneagrapher.graph import Record

# Unit tests for graph-related classes.
class TestRecordMethods(unittest.TestCase):
    """
    Unit tests for the Record class.
    """
    def test001_init(self):
        # Test the constructor.
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertEqual(record.name, "Carl Friedrich Gauss")
        self.assertEqual(record.institution, "Universitaet Helmstedt")
        self.assertEqual(record.year, 1799)
        self.assertEqual(record.id, 18231)
        
    def test002_init_bad_name(self):
        # Test constructor with bad 'name' parameter.
        self.assertRaises(TypeError, Record, 1, "Universitaet Helmstedt", 1799, 18231)
        
    def test003_init_bad_institution(self):
        # Test constructor with bad 'institution' parameter.
        self.assertRaises(TypeError, Record, "Carl Friedrich Gauss", 1, 1799, 18231)
        
    def test004_init_bad_year(self):
        # Test constructor with bad 'year' parameter.
        self.assertRaises(TypeError, Record, "Carl Friedrich Gauss",
                          "Universitaet Helmstedt", "1799", 18231)
        
    def test005_init_bad_id(self):
        # Test constructor with bad 'id' parameter.
        self.assertRaises(TypeError, Record, "Carl Friedrich Gauss",
                          "Universitaet Helmstedt", 1799, "18231")
        
    def test006_cmp_equal(self):
        # Verify two 'equal' records are compared correctly.
        record1 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record1 == record2)
        
    def test007_cmp_unequal(self):
        # Verify two 'unequal' records are compared correctly.
        record1 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        self.assert_(record1 < record2)

    def test008_has_institution_yes(self):
        # Verify has_institution() method returns True when the conditions are right.
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record.has_institution())

    def test009_has_institution_no(self):
        # Verify has_institution() method returns False when the conditions are right.
        record = Record("Carl Friedrich Gauss", None, 1799, 18231)
        self.assert_(not record.has_institution())

    def test010_has_year_yes(self):
        # Verify has_year() method returns True when the conditions are right.
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assert_(record.has_year())

    def test011_has_year_no(self):
        # Verify has_year() method returns False when the conditions are right.
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", None, 18231)
        self.assert_(not record.has_year())

if __name__ == '__main__':
    unittest.main()
