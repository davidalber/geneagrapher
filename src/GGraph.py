class DuplicateNodeError(Exception):
    def __init__(self, value):
        self.value = value
        def __str__(self):
            return repr(self.value)

class Record:
    """
    Container class storing record of a mathematician in the graph.
    """
    def __init__(self, name, institution, year, id):
        """
        Record class constructor.
        
        Parameters:
            name: string containing mathematician's name
            institution: string containing mathematician's institution
                (empty if none)
            year: integer containing year degree was earned
            id: integer containing Math Genealogy Project id value
        """
        self.name = name
        self.institution = institution
        self.year = year
        self.id = id
        
        # Verify we got the types wanted.
        if not isinstance(self.name, basestring):
            raise TypeError("Unexpected parameter type: expected string value for 'name'")
        if not isinstance(self.institution, basestring) and self.institution is not None:
            raise TypeError("Unexpected parameter type: expected string value for 'institution'")
        if not isinstance(self.year, int) and self.year is not None:
            raise TypeError("Unexpected parameter type: expected integer value for 'year'")
        if not isinstance(self.id, int):
            raise TypeError("Unexpected parameter type: expected integer value for 'id'")

    def __cmp__(self, r2):
        """
        Compare a pair of mathematician records based on ids.
        """
        return self.id.__cmp__(r2.id)
    
    def hasInstitution(self):
        """
        Return True if this record has an institution associated with it,
        else False.
        """
        return self.institution is not None
    
    def hasYear(self):
        """
        Return True if this record has a year associated with it, else
        False.
        """
        return self.year is not None
    

class Node:
    """
    Container class storing a node in the graph.
    """
    def __init__(self, record, ancestors, descendents):
        """
        Node class constructor.
        
        Parameters:
            record: instance of the Record class
            ancestors: list of the record's genealogical ancestors's
                IDs
            descendents: list of this records genealogical
                descendent's IDs
        """
        
        self.record = record
        self.ancestors = ancestors
        self.descendents = descendents
        self.already_printed = False

        # Verify parameter types.
        if not isinstance(self.record, Record):
            raise TypeError("Unexpected parameter type: expected Record object for 'record'")
        if not isinstance(self.ancestors, list):
            raise TypeError("Unexpected parameter type: expected list object for 'ancestors'")
        if not isinstance(self.descendents, list):
            raise TypeError("Unexpected parameter type: expected list object for 'descendents'")
        
    def __str__(self):
        if self.record.hasInstitution():
            if self.record.hasYear():
                return self.record.name.encode('utf-8', 'replace') + ' \\n' + self.record.institution.encode('utf-8', 'replace') + ' (' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('utf-8', 'replace') + ' \\n' + self.record.institution.encode('utf-8', 'replace')
        else:
            if self.record.hasYear():
                return self.record.name.encode('utf-8', 'replace') + ' \\n(' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('utf-8', 'replace')

    def __cmp__(self, n2):
        return self.record.__cmp__(n2.record)

    def addAncestor(self, ancestor):
        """
        Append an ancestor id to the ancestor list.
        """
        # Verify we were passed an int.
        if not isinstance(ancestor, int):
            raise TypeError("Unexpected parameter type: expected int for 'ancestor'")
        self.ancestors.append(ancestor)

    def id(self):
        """
        Accessor method to retrieve the id of this node's record.
        """
        return self.record.id


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
                self.nodes[head.id()] = head

    def hasNode(self, id):
        """
        Check if the graph contains a node with the given id.
        """
        return self.nodes.has_key(id)

    def getNode(self, id):
        """
        Return the node in the graph with given id. Returns
        None if no such node exists.
        """
        if self.hasNode(id):
            return self.nodes[id]
        else:
            return None

    def getNodeList(self):
        """
        Return a list of the nodes in the graph.
        """
        return self.nodes.keys()

    def addNode(self, name, institution, year, id, ancestors, descendents, isHead=False):
        """
        Add a new node to the graph if a matching node is not already
        present.
        """
        if not self.hasNode(id):
            record = Record(name, institution, year, id)
            node = Node(record, ancestors, descendents)
            self.nodes[id] = node
            if self.heads is None:
                self.heads = [node]
            elif isHead:
                self.heads.append(node)
        else:
            msg = "node with id %d already exists" % (id)
            raise DuplicateNodeError(msg)

    def generateDotFile(self, include_ancestors, include_descendents):
        """
        Return a string that contains the content of the Graphviz dotfile
        format for this graph.
        """
        if self.heads is None:
            return ""

        queue = []
        for head in self.heads:
            queue.append(head.id())
        edges = ""
        dotfile = ""
        
        dotfile += """digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];\n\n"""

        while len(queue) > 0:
            node_id = queue.pop()
            if not self.hasNode(node_id):
                # Skip this id if a corresponding node is not present.
                continue
            node = self.getNode(node_id)

            if node.already_printed:
                continue
            else:
                node.already_printed = True
            
            if include_ancestors:
                # Add this node's advisors to queue.
                queue += node.ancestors
                
            if include_descendents:
                # Add this node's descendents to queue.
                queue += node.descendents
        
            # Print this node's information.
            nodestr = "    %d [label=\"%s\"];" % (node_id, node)
            dotfile += nodestr

            # Store the connection information for this node.
            for advisor in node.ancestors:
                if self.hasNode(advisor):
                    edgestr = "\n    %d -> %d;" % (advisor, node_id)
                    edges += edgestr
                
            dotfile += "\n"

        # Now print the connections between the nodes.
        dotfile += edges

        dotfile += "\n}\n"
        return dotfile
