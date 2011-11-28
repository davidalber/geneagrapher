from node import Node
from record import Record


class DuplicateNodeError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Graph(dict):
    """
    Class storing the representation of a genealogy graph.
    """
    def __init__(self, seeds=None):
        """
        Graph class constructor.

        Parameters:
            seeds: a set of Node objects representing the tree seed nodes
                (omit to create an empty graph)
        """
        dict.__init__(self)
        self.seeds = seeds
        if self.seeds is None:
            self.seeds = set()
        self.supp_id = -1

        # Verify type of seeds is what we expect.
        if not isinstance(self.seeds, set):
            raise TypeError("Unexpected parameter type: expected set of \
Node objects for 'seeds'")
        for seed in self.seeds:
            if not isinstance(seed, Node):
                raise TypeError("Unexpected parameter type: expected set \
of Node objects for 'seeds'")

        if self.seeds != set():
            self.update([(seed.get_id(), seed) for seed in self.seeds])

    def has_node(self, id):
        """
        Check if the graph contains a node with the given id.
        """
        return id in self

    def get_node(self, id):
        """
        Return the node in the graph with given id. Returns
        None if no such node exists.
        """
        return self[id]

    def get_node_list(self):  # NOTE: this method is unused
        """
        Return a list of the nodes in the graph.
        """
        return self.keys()

    def add_node(self, name, institution, year, id, ancestors, descendants,
                 is_seed=False):
        """
        Add a new node to the graph if a matching node is not already
        present.
        """
        record = Record(name, institution, year, id)
        node = Node(record, ancestors, descendants)
        self.add_node_object(node, is_seed)

    def add_node_object(self, node, is_seed=False):
        """
        Add a new node object to the graph if a node with the same id
        is not already present.
        """
        if node.get_id() is not None and self.has_node(node.get_id()):
            msg = "node with id {} already exists".format(node.get_id())
            raise DuplicateNodeError(msg)
        if node.get_id() is None:
            # Assign a "dummy" id.
            node.set_id(self.supp_id)
            self.supp_id -= 1
        self[node.get_id()] = node
        if self.seeds == set() or is_seed:
            self.seeds.add(node)

    def generate_dot_file(self, include_ancestors, include_descendants):
        """
        Return a string that contains the content of the Graphviz dotfile
        format for this graph.
        """
        if self.seeds == set():
            return ""

        queue = []
        for seed in self.seeds:
            queue.append(seed.get_id())
        edges = ""
        dotfile = ""

        dotfile += u"""digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];\n\n"""

        printed_nodes = {}
        while len(queue) > 0:
            node_id = queue.pop(0)
            if not self.has_node(node_id):
                # Skip this id if a corresponding node is not present.
                continue
            if node_id in printed_nodes:
                # Skip this id because it is already printed.
                continue
            node = self.get_node(node_id)
            printed_nodes[node_id] = node

            sorted_ancestors = sorted([a for a in node.ancestors if a in self],
                                      lambda x, y:
                                      cmp(self[x].record.name.split()[-1],
                                          self[y].record.name.split()[-1]))
            sorted_descendants = sorted([d for d in node.descendants if
                                         d in self],
                                        lambda x, y:
                                        cmp(self[x].record.name.split()[-1],
                                            self[y].record.name.split()[-1]))

            if include_ancestors:
                # Add this node's advisors to queue.
                queue += sorted_ancestors

            if include_descendants:
                # Add this node's descendants to queue.
                queue += sorted_descendants

            # Print this node's information.
            nodestr = u"    {} [label=\"{}\"];".format(node_id, node)
            dotfile += nodestr

            # Store the connection information for this node.
            for advisor in sorted_ancestors:
                if self.has_node(advisor):
                    edgestr = "\n    {} -> {};".format(advisor, node_id)
                    edges += edgestr

            dotfile += "\n"

        # Now print the connections between the nodes.
        dotfile += edges

        dotfile += "\n}\n"
        return dotfile
