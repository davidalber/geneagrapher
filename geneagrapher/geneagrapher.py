from argparse import ArgumentParser
from collections import deque
import pkg_resources
import sys
from cache_grabber import CacheGrabber
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
        self.use_cache = True
        self.cache_file = "geneacache"

    def parse_input(self):
        """
        Parse command-line information.
        """
        pkg_env = pkg_resources.Environment()
        description = 'Create a Graphviz "dot" file for a mathematics \
genealogy, where ID is a record identifier from the Mathematics Genealogy \
Project. Multiple IDs may be passed.'
        self.parser = ArgumentParser(description=description)

        try:
            version = "{}".format(pkg_env[self.__module__.split(".")[0]][0].version)
        except IndexError:
            version = "dev"
        self.parser.add_argument(
            "--version", action="version", version="%(prog)s {0}".format(version)
        )
        self.parser.add_argument(
            "-f",
            "--file",
            dest="filename",
            help="write output to FILE [default: stdout]",
            metavar="FILE",
            default=None,
        )
        self.parser.add_argument(
            "-a",
            "--with-ancestors",
            action="store_true",
            dest="get_ancestors",
            default=False,
            help="retrieve ancestors of IDs and include \
in graph",
        )
        self.parser.add_argument(
            "-d",
            "--with-descendants",
            action="store_true",
            dest="get_descendants",
            default=False,
            help="retrieve descendants of IDs and \
include in graph",
        )
        self.parser.add_argument(
            "--disable-cache",
            action="store_false",
            dest="use_cache",
            default=True,
            help="do not store records in local cache",
        )
        self.parser.add_argument(
            "--cache-file",
            dest="cache_file",
            help="write cache to FILE [default: \
geneacache]",
            metavar="FILE",
            default="geneacache",
        )
        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="list nodes being retrieved",
        )
        self.parser.add_argument(
            "ids", metavar="ID", type=int, nargs="+", help="mathematician record ID"
        )

        args = self.parser.parse_args()

        self.get_ancestors = args.get_ancestors
        self.get_descendants = args.get_descendants
        self.verbose = args.verbose
        self.write_filename = args.filename
        self.use_cache = args.use_cache
        self.cache_file = args.cache_file
        self.seed_ids = [int(arg) for arg in args.ids]

    def build_graph_portion(self, grab_queue, is_seed, grabber, **kwargs):
        """Handle grabbing and storing nodes in the graph. Depending on the
        arguments, this method handles seed nodes, ancestors, or
        descendants."""
        while len(grab_queue) != 0:
            id = grab_queue.popleft()
            if not self.graph.has_node(id):
                # Then this information has not yet been grabbed.
                if self.verbose:
                    sys.stdout.write("Grabbing record #{}...".format(id))
                record = grabber.get_record(id)
                if self.verbose:
                    if "message" in record:
                        print record["message"]
                    else:
                        print
                self.graph.add_node(
                    record["name"],
                    record["institution"],
                    record["year"],
                    id,
                    record["advisors"],
                    record["descendants"],
                    is_seed,
                )
                if self.get_ancestors and "ancestor_queue" in kwargs:
                    kwargs["ancestor_queue"].extend(record["advisors"])
                if self.get_descendants and "descendant_queue" in kwargs:
                    kwargs["descendant_queue"].extend(record["descendants"])

    def build_graph_complete(self, record_grabber=Grabber, **kwargs):
        """
        Populate the graph member by grabbing the mathematician
        pages and extracting relevant data.
        """
        seed_queue = deque(self.seed_ids)
        ancestor_queue = deque()
        descendant_queue = deque()
        with record_grabber(**kwargs) as grabber:
            # Grab "seed" nodes.
            self.build_graph_portion(
                seed_queue,
                True,
                grabber,
                ancestor_queue=ancestor_queue,
                descendant_queue=descendant_queue,
            )

            # Grab ancestors of seed nodes.
            if self.get_ancestors:
                self.build_graph_portion(
                    ancestor_queue, False, grabber, ancestor_queue=ancestor_queue
                )

            # Grab descendants of seed nodes.
            if self.get_descendants:
                self.build_graph_portion(
                    descendant_queue, False, grabber, descendant_queue=descendant_queue
                )

    def build_graph(self):
        """Call the graph builder method with the correct arguments, based
        on the command-line arguments."""
        if self.use_cache:
            record_grabber = CacheGrabber
        else:
            record_grabber = Grabber
        self.build_graph_complete(record_grabber, filename=self.cache_file)

    def generate_dot_file(self):
        dotfile = self.graph.generate_dot_file(self.get_ancestors, self.get_descendants)
        dotfile = dotfile.encode("utf-8", "replace")
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

    try:
        ggrapher.build_graph()
    except ValueError as e:
        print e
    ggrapher.generate_dot_file()


if __name__ == "__main__":
    ggrapher()
