import os
import sys
import unittest
import StringIO
from geneagrapher import geneagrapher
from geneagrapher.cache_grabber import CacheGrabber
from geneagrapher.graph import Graph
from local_data_grabber import LocalDataGrabber


class TestGeneagrapherMethods(unittest.TestCase):
    """Unit tests for the geneagrapher.Geneagrapher class."""
    def setUp(self):
        self.ggrapher = geneagrapher.Geneagrapher()

    def test_init(self):
        """Test constructor."""
        self.assertEqual(isinstance(self.ggrapher.graph, Graph), True)
        self.assertEqual(self.ggrapher.seed_ids, [])
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.use_cache, True)
        self.assertEqual(self.ggrapher.cache_file, 'geneacache')

    def test_parse_empty(self):
        """Test parse_input() with no arguments."""
        sys.argv = ['geneagrapher']

        # Redirect stderr to capture output.
        stderr = sys.stderr
        stderr_intercept = StringIO.StringIO()
        sys.stderr = stderr_intercept

        expected = """usage: geneagrapher [-h] [--version] [-f FILE] [-a] \
[-d] [--disable-cache]
                    [--cache-file FILE] [-v]
                    ID [ID ...]
geneagrapher: error: too few arguments
"""
        try:
            self.ggrapher.parse_input()
        except SystemExit:
            self.assertEqual(stderr_intercept.getvalue().decode('utf-8'),
                             expected)

        sys.stderr = stderr

    def test_parse_default(self):
        """Test parse_input() with no options."""
        sys.argv = ['geneagrapher', '3']
        self.ggrapher.get_ancestors = False
        self.ggrapher.get_descendents = True
        self.ggrapher.write_filename = "filler"
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.use_cache, True)
        self.assertEqual(self.ggrapher.cache_file, 'geneacache')
        self.assertEqual(self.ggrapher.seed_ids, [3])

    def test_parse_options(self):
        """Test parse_input() with options."""
        sys.argv = ['geneagrapher', '--with-ancestors', '--with-descendants',
                    '--file=filler', '--verbose', '--disable-cache',
                    '--cache-file', 'foo', '3', '43']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, True)
        self.assertEqual(self.ggrapher.get_descendants, True)
        self.assertEqual(self.ggrapher.verbose, True)
        self.assertEqual(self.ggrapher.write_filename, "filler")
        self.assertEqual(self.ggrapher.use_cache, False)
        self.assertEqual(self.ggrapher.cache_file, 'foo')
        self.assertEqual(self.ggrapher.seed_ids, [3, 43])

    def test_parse_short_options(self):
        """Test parse_input() with short versions of the options."""
        sys.argv = ['geneagrapher', '-a', '-d', '-f', 'filler', '-v', '3',
                    '43']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, True)
        self.assertEqual(self.ggrapher.get_descendants, True)
        self.assertEqual(self.ggrapher.verbose, True)
        self.assertEqual(self.ggrapher.write_filename, "filler")
        self.assertEqual(self.ggrapher.use_cache, True)
        self.assertEqual(self.ggrapher.cache_file, 'geneacache')
        self.assertEqual(self.ggrapher.seed_ids, [3, 43])

    def test_build_graph_complete_only_self(self):
        """Graph building with no ancestors or descendants."""
        self.ggrapher.seed_ids.append(127946)
        self.ggrapher.build_graph_complete(LocalDataGrabber)
        graph = self.ggrapher.graph
        self.assertEqual(len(graph), 1)
        self.assertTrue(127946 in graph)

        node = graph[127946]
        self.assertEqual(node.ancestors, set())
        self.assertEqual(node.descendants, set())

        record = node.record
        self.assertEqual(record.name, "Christian   Thomasius")
        self.assertEqual(record.institution, None)
        self.assertEqual(record.year, 1672)
        self.assertEqual(record.id, 127946)

    def test_build_graph_complete_only_self_verbose_cache_grabber(self):
        """Graph building with no ancestors or descendants using the cache
        grabber to verify its verbose printing."""
        self.ggrapher.verbose = True
        self.ggrapher.seed_ids.append(127946)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        cache_fname = LocalDataGrabber.data_file(
            'geneagrapher_verbose_cache_grabber_test')
        expiration = 1e15
        self.ggrapher.build_graph_complete(CacheGrabber, filename=cache_fname,
                                           expiration_interval=expiration)
        sys.stdout = stdout

        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'),
                         u"Grabbing record #127946...cache hit\n")

    def test_build_graph_complete_only_self_verbose_error(self):
        """Graph building with no ancestors or descendants given a bad
        ID."""
        self.ggrapher.verbose = True
        self.ggrapher.seed_ids.append(999999999)

        self.assertRaises(ValueError, self.ggrapher.build_graph_complete,
                          LocalDataGrabber)

    def test_build_graph_complete_only_self_verbose_error_long(self):
        """Graph building with no ancestors or descendants given a bad
        ID of the long variety."""
        self.ggrapher.verbose = True
        self.ggrapher.seed_ids.append(999999999999999999999)

        self.assertRaises(ValueError, self.ggrapher.build_graph_complete,
                          LocalDataGrabber)

    def test_build_graph_complete_only_self_verbose(self):
        """Graph building with no ancestors or descendants."""
        self.ggrapher.verbose = True
        self.ggrapher.seed_ids.append(127946)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        self.ggrapher.build_graph_complete(LocalDataGrabber)
        sys.stdout = stdout

        graph = self.ggrapher.graph
        self.assertEqual(len(graph), 1)
        self.assertTrue(127946 in graph)

        node = graph[127946]
        self.assertEqual(node.ancestors, set())
        self.assertEqual(node.descendants, set())

        record = node.record
        self.assertEqual(record.name, "Christian   Thomasius")
        self.assertEqual(record.institution, None)
        self.assertEqual(record.year, 1672)
        self.assertEqual(record.id, 127946)

        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'),
                         u"Grabbing record #127946...\n")

    def test_build_graph_complete_with_ancestors(self):
        """Graph building with ancestors."""
        self.ggrapher.seed_ids.append(127946)
        self.ggrapher.get_ancestors = True
        self.ggrapher.build_graph_complete(LocalDataGrabber)
        graph = self.ggrapher.graph
        self.assertEqual(len(graph), 4)
        self.assertTrue(127946 in graph)
        self.assertTrue(137717 in graph)
        self.assertTrue(137705 in graph)
        self.assertTrue(143630 in graph)

        node = graph[127946]
        self.assertEqual(node.ancestors, set([137717, 137705]))
        self.assertEqual(node.descendants, set())

        record = node.record
        self.assertEqual(record.name, "Christian   Thomasius")
        self.assertEqual(record.institution, None)
        self.assertEqual(record.year, 1672)
        self.assertEqual(record.id, 127946)

        node = graph[137717]
        self.assertEqual(node.ancestors, set([]))
        self.assertEqual(node.descendants, set([127946]))

        record = node.record
        self.assertEqual(record.name, "Valentin  Alberti")
        self.assertEqual(record.institution, u"Universit\xe4t Leipzig")
        self.assertEqual(record.year, 1678)
        self.assertEqual(record.id, 137717)

        node = graph[137705]
        self.assertEqual(node.ancestors, set([143630]))
        self.assertEqual(node.descendants, set([127946]))

        record = node.record
        self.assertEqual(record.name, "Jakob  Thomasius")
        self.assertEqual(record.institution, u"Universit\xe4t Leipzig")
        self.assertEqual(record.year, 1643)
        self.assertEqual(record.id, 137705)

        node = graph[143630]
        self.assertEqual(node.ancestors, set([]))
        self.assertEqual(node.descendants, set([137705]))

        record = node.record
        self.assertEqual(record.name, "Friedrich  Leibniz")
        self.assertEqual(record.institution, None)
        self.assertEqual(record.year, None)
        self.assertEqual(record.id, 143630)

    def test_build_graph_complete_with_descendants(self):
        """Graph building with descendants."""
        self.ggrapher.seed_ids.append(79568)
        self.ggrapher.get_descendants = True
        self.ggrapher.build_graph_complete(LocalDataGrabber)
        graph = self.ggrapher.graph
        self.assertEqual(len(graph), 3)
        self.assertTrue(79568 in graph)
        self.assertTrue(79562 in graph)
        self.assertTrue(99457 in graph)

        node = graph[79568]
        self.assertEqual(node.ancestors, set())
        self.assertEqual(node.descendants, set([79562, 99457]))

        record = node.record
        self.assertEqual(record.name, "Ramdas  Kumaresan")
        self.assertEqual(record.institution, u"University of Rhode Island")
        self.assertEqual(record.year, 1982)
        self.assertEqual(record.id, 79568)

        node = graph[79562]
        self.assertEqual(node.ancestors, set([79568]))
        self.assertEqual(node.descendants, set([]))

        record = node.record
        self.assertEqual(record.name, "C. S. Ramalingam")
        self.assertEqual(record.institution, u"University of Rhode Island")
        self.assertEqual(record.year, 1995)
        self.assertEqual(record.id, 79562)

        node = graph[99457]
        self.assertEqual(node.ancestors, set([79568]))
        self.assertEqual(node.descendants, set([]))

        record = node.record
        self.assertEqual(record.name, "Yadong  Wang")
        self.assertEqual(record.institution, u"University of Rhode Island")
        self.assertEqual(record.year, 2003)
        self.assertEqual(record.id, 99457)

    def test_build_graph_complete_bad_id(self):
        """Graph building with a bad ID."""
        self.ggrapher.seed_ids.append(79568583832)
        self.assertRaises(ValueError, self.ggrapher.build_graph_complete,
                          LocalDataGrabber)

        try:
            self.ggrapher.build_graph_complete(LocalDataGrabber)
        except ValueError as e:
            self.assertEqual(str(e), "Invalid id 79568583832")
        else:
            self.fail()

    def test_end_to_end_self_stdout(self):
        """Complete test getting no ancestors or descendants and writing the
        result to stdout."""
        sys.argv = ['geneagrapher', '30484']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.seed_ids, [30484])

        self.ggrapher.build_graph_complete(LocalDataGrabber)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        self.ggrapher.generate_dot_file()
        sys.stdout = stdout

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    30484 [label="Peter Chris Pappas \\nThe Pennsylvania State University \
(1982)"];

}
"""
        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'), expected)

    def test_end_to_end_cached_self_stdout(self):
        """Complete test using cache getting no ancestors or descendants and
        writing the result to stdout."""
        cache_fname = LocalDataGrabber.data_file(
            'end-to-end-30484')
        sys.argv = ['geneagrapher', '--cache-file', cache_fname, '30484']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.seed_ids, [30484])

        self.ggrapher.build_graph_complete(CacheGrabber,
                                           filename=self.ggrapher.cache_file)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        self.ggrapher.generate_dot_file()
        sys.stdout = stdout

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    30484 [label="Peter Chris Pappas \\nThe Pennsylvania State University \
(1982)"];

}
"""
        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'), expected)

    def test_end_to_end_ancestors_stdout(self):
        """
        Complete test getting with ancestors, writing the result to stdout.
        """
        sys.argv = ['geneagrapher', '-a', '127946']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, True)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.seed_ids, [127946])

        self.ggrapher.build_graph_complete(LocalDataGrabber)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        self.ggrapher.generate_dot_file()
        sys.stdout = stdout

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    127946 [label="Christian   Thomasius \\n(1672)"];
    137717 [label="Valentin  Alberti \\nUniversit\xe4t Leipzig (1678)"];
    137705 [label="Jakob  Thomasius \\nUniversit\xe4t Leipzig (1643)"];
    143630 [label="Friedrich  Leibniz"];

    137717 -> 127946;
    137705 -> 127946;
    143630 -> 137705;
}
"""
        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'), expected)

    def test_end_to_end_descendants_stdout(self):
        """
        Complete test getting with descendants, writing the result to stdout.
        """
        sys.argv = ['geneagrapher', '-d', '79568']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, True)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, None)
        self.assertEqual(self.ggrapher.seed_ids, [79568])

        self.ggrapher.build_graph_complete(LocalDataGrabber)

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        self.ggrapher.generate_dot_file()
        sys.stdout = stdout

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    79568 [label="Ramdas  Kumaresan \\nUniversity of Rhode Island (1982)"];
    79562 [label="C. S. Ramalingam \\nUniversity of Rhode Island (1995)"];
    99457 [label="Yadong  Wang \\nUniversity of Rhode Island (2003)"];

    79568 -> 79562;
    79568 -> 99457;
}
"""
        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'), expected)

    def test_end_to_end_self_file(self):
        """Complete test getting no ancestors or descendants and writing the
        # result to stdout."""
        outfname = 'outfile.test'
        sys.argv = ['geneagrapher', '-f', outfname, '30484']
        self.ggrapher.parse_input()
        self.assertEqual(self.ggrapher.get_ancestors, False)
        self.assertEqual(self.ggrapher.get_descendants, False)
        self.assertEqual(self.ggrapher.verbose, False)
        self.assertEqual(self.ggrapher.write_filename, outfname)
        self.assertEqual(self.ggrapher.seed_ids, [30484])

        self.ggrapher.build_graph_complete(LocalDataGrabber)
        self.ggrapher.generate_dot_file()

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    30484 [label="Peter Chris Pappas \\nThe Pennsylvania State University \
(1982)"];

}
"""
        with open(outfname, 'r') as fin:
            self.assertEqual(fin.read().decode('utf-8'), expected)
        os.remove(outfname)

    def test_end_to_end_through_ggrapher_self_stdout(self):
        """Complete test calling ggrapher getting no ancestors or descendants
        and writing the result to stdout."""
        cache_fname = LocalDataGrabber.data_file(
            'end-to-end-30484')
        sys.argv = ['geneagrapher', '--cache-file', cache_fname, '30484']

        # Redirect stdout to capture output.
        stdout = sys.stdout
        stdout_intercept = StringIO.StringIO()
        sys.stdout = stdout_intercept
        geneagrapher.ggrapher()
        sys.stdout = stdout

        expected = u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];

    30484 [label="Peter Chris Pappas \\nThe Pennsylvania State University \
(1982)"];

}
"""
        self.assertEqual(stdout_intercept.getvalue().decode('utf-8'), expected)

if __name__ == '__main__':
    unittest.main()
