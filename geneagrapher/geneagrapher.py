from optparse import OptionParser
import pkg_resources
from graph import Graph
from grabber import Grabber

class Geneagrapher:
    """
    A class for building Graphviz "dot" files for math genealogies
    extracted from the Mathematics Genealogy Project website.
    """
    def __init__(self):
        self.graph = Graph()
        self.leaf_ids = []
        self.get_ancestors = False
        self.get_descendants = False
        self.verbose = False
        self.write_filename = None

    def parse_input(self):
        """
        Parse command-line information.
        """
        pkg_env = pkg_resources.Environment()
        self.parser = OptionParser(version="{}".format(
            pkg_env[self.__module__.split('.')[0]][0].version))

        self.parser.set_usage("%prog [options] ID [ID...]")
        self.parser.set_description('Create a Graphviz "dot" file for a mathematics genealogy, where ID is a record identifier from the Mathematics Genealogy Project. Multiple IDs may be passed.')

        self.parser.add_option("-f", "--file", dest="filename",
			       help="write output to FILE [default: stdout]",
			       metavar="FILE", default=None)
        self.parser.add_option("-a", "--with-ancestors", action="store_true",
			       dest="get_ancestors", default=False,
			       help="retrieve ancestors of IDs and include in graph")
        self.parser.add_option("-d", "--with-descendants", action="store_true",
			       dest="get_descendants", default=False,
			       help="retrieve descendants of IDs and include in graph")
        self.parser.add_option("--verbose", "-v", action="store_true", dest="verbose",
			       default=False, help="list nodes being retrieved")

        (options, args) = self.parser.parse_args()
        
        if len(args) == 0:
            self.parser.error("no record IDs given")

        self.get_ancestors = options.get_ancestors
        self.get_descendants = options.get_descendants
        self.verbose = options.verbose
        self.write_filename = options.filename
        self.leaf_ids = [int(arg) for arg in args]

    def build_graph_portion(self, grab_queue, is_seed, **kwargs):
        """Handle grabbing and storing nodes in the graph. Depending on the
        arguments, this method handles seed nodes, ancestors, or descendants."""
        while len(grab_queue) != 0:
            id = grab_queue.pop(0)
            if not self.graph.has_node(id):
                # Then this information has not yet been grabbed.
                grabber = Grabber(id)
                if self.verbose:
                    print "Grabbing record #{}".format(id)
                [name, institution, year, advisors, descendants] = grabber.extract_node_information()
                self.graph.add_node(name, institution, year, id, advisors, descendants, is_seed)
                if self.get_ancestors and kwargs.has_key('ancestor_grab_queue'):
                    kwargs['ancestor_grab_queue'] += advisors
                if self.get_descendants and kwargs.has_key('descendant_grab_queue'):
                    kwargs['descendant_grab_queue'] += descendants
        
    def build_graph(self):
        """
        Populate the graph member by grabbing the mathematician
        pages and extracting relevant data.
        """
        leaf_grab_queue = list(self.leaf_ids)
        ancestor_grab_queue = []
        descendant_grab_queue = []

        # Grab "leaf" nodes.
        self.build_graph_portion(leaf_grab_queue, True,
                                 ancestor_grab_queue=ancestor_grab_queue,
                                 descendant_grab_queue=descendant_grab_queue)

        # Grab ancestors of leaf nodes.
        if self.get_ancestors:
            self.build_graph_portion(ancestor_grab_queue, False,
                                     ancestor_grab_queue=ancestor_grab_queue)

        # Grab descendants of leaf nodes.
        if self.get_descendants:
            self.build_graph_portion(descendant_grab_queue, False,
                                     descendant_grab_queue=descendant_grab_queue)

    def generate_dot_file(self):
        dotfile = self.graph.generate_dot_file(self.get_ancestors, self.get_descendants)
        dotfile = dotfile.encode('utf-8', 'replace')
        if self.write_filename is not None:
            outfile = open(self.write_filename, "w")
            outfile.write(dotfile)
            outfile.close()
        else:
            print dotfile,
        
def ggrapher():
    """Function to run the Geneagrapher. This is the function called when
    the ggrapher script is run."""
    ggrapher = Geneagrapher()
    ggrapher.parse_input()
    ggrapher.build_graph()
    ggrapher.generate_dot_file()
