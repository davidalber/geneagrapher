import unittest
from test_record_methods import TestRecordMethods
from test_node_methods import TestNodeMethods
from test_graph_methods import TestGraphMethods
from test_grabber_methods import TestGrabberMethods
from test_geneagrapher_methods import TestGeneagrapherMethods

def runTests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRecordMethods))
    suite.addTest(unittest.makeSuite(TestNodeMethods))
    suite.addTest(unittest.makeSuite(TestGraphMethods))
    suite.addTest(unittest.makeSuite(TestGrabberMethods))
    suite.addTest(unittest.makeSuite(TestGeneagrapherMethods))
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':
    runTests()
