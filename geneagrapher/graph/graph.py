from node import Node
from record import Record

class DuplicateNodeError(Exception):
    def __init__(self, value):
        self.value = value
        def __str__(self):
            return repr(self.value)

class Graph:
    """
    Class storing the representation of a genealogy graph.
    """
    def __init__(self, heads=None):
        """
        Graph class constructor.
        
        Parameters:
            heads: a list of Node objects representing the tree head
                (can be omitted to create an empty graph)
        """
        self.heads = heads
        self.supp_id = -1
        
        # Verify type of heads is what we expect.
        if self.heads is not None:
            if not isinstance(self.heads, list):
                raise TypeError("Unexpected parameter type: expected list of Node objects for 'heads'")
            for head in self.heads:
                if not isinstance(head, Node):
                    raise TypeError("Unexpected parameter type: expected list of Node objects for 'heads'")

        self.nodes = {}
        if self.heads is not None:
            for head in self.heads:
                self.nodes[head.get_id()] = head

    def has_node(self, id):
        """
        Check if the graph contains a node with the given id.
        """
        return self.nodes.has_key(id)

    def get_node(self, id):
        """
        Return the node in the graph with given id. Returns
        None if no such node exists.
        """
        if self.has_node(id):
            return self.nodes[id]
        else:
            return None

    def get_node_list(self): # NOTE: this method is unused
        """
        Return a list of the nodes in the graph.
        """
        return self.nodes.keys()

    def add_node(self, name, institution, year, id, ancestors, descendants, isHead=False):
        """
        Add a new node to the graph if a matching node is not already
        present.
        """
        record = Record(name, institution, year, id)
        node = Node(record, ancestors, descendants)
        self.add_node_object(node, isHead)

    def add_node_object(self, node, isHead=False):
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
        self.nodes[node.get_id()] = node
        if self.heads is None:
            self.heads = [node]
        elif isHead:
            self.heads.append(node)

    def generate_dot_file(self, include_ancestors, include_descendants):
        """
        Return a string that contains the content of the Graphviz dotfile
        format for this graph.
        """
        if self.heads is None:
            return ""

        queue = []
        for head in self.heads:
            queue.append(head.get_id())
        edges = ""
        dotfile = ""
        
        dotfile += """digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];\n\n"""

        while len(queue) > 0:
            node_id = queue.pop()
            if not self.has_node(node_id):
                # Skip this id if a corresponding node is not present.
                continue
            node = self.get_node(node_id)

            if node.already_printed:
                continue
            else:
                node.already_printed = True
            
            if include_ancestors:
                # Add this node's advisors to queue.
                queue += node.ancestors
                
            if include_descendants:
                # Add this node's descendants to queue.
                queue += node.descendants
        
            # Print this node's information.
            nodestr = "    {} [label=\"{}\"];".format(node_id, node)
            dotfile += nodestr

            # Store the connection information for this node.
            for advisor in node.ancestors:
                if self.has_node(advisor):
                    edgestr = "\n    {} -> {};".format(advisor, node_id)
                    edges += edgestr
                
            dotfile += "\n"

        # Now print the connections between the nodes.
        dotfile += edges

        dotfile += "\n}\n"
        return dotfile
