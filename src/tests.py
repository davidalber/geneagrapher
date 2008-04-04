import unittest
import GGraph

# Unit tests for GGraph.
class TestRecordMethods(unittest.TestCase):
    """
    Unit tests for the GGraph.Record class.
    """

    def test001_init(self):
        # Test constructor.
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
        

if __name__ == '__main__':
    unittest.main()