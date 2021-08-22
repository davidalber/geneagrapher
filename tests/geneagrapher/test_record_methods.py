import unittest
from geneagrapher.graph import Record


# Unit tests for graph-related classes.
class TestRecordMethods(unittest.TestCase):
    """Unit tests for the Record class."""

    def setUp(self):
        self.record = Record(
            "Carl Friedrich Gau\xdf", "Universit\xe4t Helmstedt", 1799, 18231)

    def test_init(self):
        """Test the constructor."""
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertEqual(record.name, "Carl Friedrich Gauss")
        self.assertEqual(record.institution, "Universitaet Helmstedt")
        self.assertEqual(record.year, 1799)
        self.assertEqual(record.id, 18231)

    def test_init_bad_name(self):
        """Test constructor with bad 'name' parameter."""
        self.assertRaises(TypeError, Record, 1, "Universitaet Helmstedt", 1799, 18231)

    def test_init_bad_institution(self):
        """Test constructor with bad 'institution' parameter."""
        self.assertRaises(TypeError, Record, "Carl Friedrich Gauss", 1, 1799, 18231)

    def test_init_bad_year(self):
        """Test constructor with bad 'year' parameter."""
        self.assertRaises(
            TypeError,
            Record,
            "Carl Friedrich Gauss",
            "Universitaet Helmstedt",
            "1799",
            18231,
        )

    def test_init_bad_id(self):
        """Test constructor with bad 'id' parameter."""
        self.assertRaises(
            TypeError,
            Record,
            "Carl Friedrich Gauss",
            "Universitaet Helmstedt",
            1799,
            "18231",
        )

    def test_equal(self):
        """Verify two 'equal' records are compared correctly."""
        record1 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertTrue(record1 == record2)

    def test_unequal(self):
        """Verify two 'unequal' records are compared correctly."""
        record1 = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        record2 = Record("Leonhard Euler", "Universitaet Basel", 1726, 38586)
        self.assertTrue(record1 < record2)
        self.assertTrue(record1 != record2)
        self.assertTrue(record2 > record1)

    def test_has_institution_yes(self):
        """Verify has_institution() method returns True when the conditions are
        right."""
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertTrue(record.has_institution())
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertTrue(record.has_institution())

    def test_has_institution_no(self):
        """Verify has_institution() method returns False when the conditions
        are right."""
        record = Record("Carl Friedrich Gauss", None, 1799, 18231)
        self.assertTrue(not record.has_institution())

    def test_has_year_yes(self):
        """
        Verify has_year() method returns True when the conditions are right.
        """
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", 1799, 18231)
        self.assertTrue(record.has_year())

    def test_has_year_no(self):
        """
        Verify has_year() method returns False when the conditions are right.
        """
        record = Record("Carl Friedrich Gauss", "Universitaet Helmstedt", None, 18231)
        self.assertTrue(not record.has_year())

    def test_str_full(self):
        """Test __str__() method for complete record."""
        recstr = str(self.record)
        recstrexpt = "Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt \
(1799)"
        self.assertEqual(recstr, recstrexpt)

    def test_no_year(self):
        """Test __str__() method for record without year."""
        record = Record(self.record.name, self.record.institution, None, 18231)
        recstr = str(record)
        recstrexpt = "Carl Friedrich Gau\xdf \\nUniversit\xe4t Helmstedt"
        self.assertEqual(recstr, recstrexpt)

    def test_no_inst(self):
        """Test __str__() method for record without institution."""
        record = Record(self.record.name, None, 1799, 18231)
        recstr = str(record)
        recstrexpt = "Carl Friedrich Gau\xdf \\n(1799)"
        self.assertEqual(recstr, recstrexpt)

    def test_no_inst_no_id(self):
        """Test __unicode__() method for record without institution or year."""
        record = Record(self.record.name, None, None, 18231)
        recstr = str(record)
        recstrexpt = "Carl Friedrich Gau\xdf"
        self.assertEqual(recstr, recstrexpt)


if __name__ == "__main__":
    unittest.main()
