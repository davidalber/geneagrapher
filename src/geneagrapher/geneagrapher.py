from optparse import OptionParser
from collections import deque
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
        self.seed_ids = []
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
        self.parser.set_description('Create a Graphviz "dot" file for a \
mathematics genealogy, where ID is a record identifier from the Mathematics \
Genealogy Project. Multiple IDs may be passed.')

        self.parser.add_option("-f", "--file", dest="filename",
                               help="write output to FILE [default: stdout]",
                               metavar="FILE", default=None)
        self.parser.add_option("-a", "--with-ancestors", action="store_true",
                               dest="get_ancestors", default=False,
                               help="retrieve ancestors of IDs and include in \
graph")
        self.parser.add_option("-d", "--with-descendants", action="store_true",
                               dest="get_descendants", default=False,
                               help="retrieve descendants of IDs and include \
in graph")
        self.parser.add_option("--verbose", "-v", action="store_true",
                               dest="verbose", default=False,
                               help="list nodes being retrieved")

        (options, args) = self.parser.parse_args()

        if len(args) == 0:
            self.parser.error("no record IDs given")

        self.get_ancestors = options.get_ancestors
        self.get_descendants = options.get_descendants
        self.verbose = options.verbose
        self.write_filename = options.filename
        self.seed_ids = [int(arg) for arg in args]

    def build_graph_portion(self, grab_queue, is_seed, grabber, **kwargs):
        """Handle grabbing and storing nodes in the graph. Depending on the
        arguments, this method handles seed nodes, ancestors, or
        descendants."""
        while len(grab_queue) != 0:
            id = grab_queue.popleft()
            if not self.graph.has_node(id):
                # Then this information has not yet been grabbed.
                if self.verbose:
                    print "Grabbing record #{}".format(id)
                [name, institution, year, advisors,
                 descendants] = grabber.get_record(id)
                self.graph.add_node(name, institution, year, id, advisors,
                                    descendants, is_seed)
                if self.get_ancestors and 'ancestor_queue' in kwargs:
                    kwargs['ancestor_queue'].extend(advisors)
                if self.get_descendants and 'descendant_queue' in kwargs:
                    kwargs['descendant_queue'].extend(descendants)

    def build_graph(self, record_grabber=Grabber, **kwargs):
        """
        Populate the graph member by grabbing the mathematician
        pages and extracting relevant data.
        """
        seed_queue = deque(self.seed_ids)
        ancestor_queue = deque()
        descendant_queue = deque()
        with record_grabber(**kwargs) as grabber:
            # Grab "seed" nodes.
            self.build_graph_portion(seed_queue, True, grabber,
                                     ancestor_queue=ancestor_queue,
                                     descendant_queue=descendant_queue)

            # Grab ancestors of seed nodes.
            if self.get_ancestors:
                self.build_graph_portion(ancestor_queue, False, grabber,
                                         ancestor_queue=ancestor_queue)

            # Grab descendants of seed nodes.
            if self.get_descendants:
                self.build_graph_portion(descendant_queue, False, grabber,
                                         descendant_queue=descendant_queue)

    def generate_dot_file(self):
        dotfile = self.graph.generate_dot_file(self.get_ancestors,
                                               self.get_descendants)
        dotfile = dotfile.encode('utf-8', 'replace')
        if self.write_filename is not None:
            outfile = open(self.write_filename, "w")
            outfile.write(dotfile)
            outfile.close()
        else:
            print dotfile,


def ggrapher(record_grabber=Grabber):
    """Function to run the Geneagrapher. This is the function called when
    the ggrapher script is run."""
    ggrapher = Geneagrapher()
    ggrapher.parse_input()
    ggrapher.build_graph(record_grabber)
    ggrapher.generate_dot_file()
