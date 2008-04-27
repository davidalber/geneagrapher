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
        if not isinstance(self.institution, basestring):
            raise TypeError("Unexpected parameter type: expected string value for 'institution'")
        if not isinstance(self.year, int):
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
        return self.institution != ""
    
    def hasYear(self):
        """
        Return True if this record has a year associated with it, else
        False.
        """
        return self.year != -1
    

class Node:
    """
    Container class storing a node in the graph.
    """
    def __init__(self, record, ancestors):
        """
        Node class constructor.
        
        Parameters:
            record: instance of the Record class
            ancestors: list of Node objects containing this node's
                genealogical ancestors
        """
        
        self.record = record
        self.ancestors = ancestors
        self.already_printed = False

        # Verify parameter types.
        if not isinstance(self.record, Record):
            raise TypeError("Unexpected parameter type: expected Record object for 'record'")
        if not isinstance(self.ancestors, list):
            raise TypeError("Unexpected parameter type: expected list object for 'ancestors'")
        
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
    def __init__(self, head=None):
        """
        Graph class constructor.
        
        Parameters:
            head: a Node object representing the tree head (can be
                omitted to create an empty graph)
        """
        self.head = head
        
        # Verify type of head is what we expect.
        if self.head is not None and not isinstance(self.head, Node):
            raise TypeError("Unexpected parameter type: expected Node object for 'head'")

        if self.head is not None:
            self.nodes = {head.id(): head}
        else:
            self.nodes = {}

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

    def addNode(self, name, institution, year, id, ancestors):
        """
        Add a new node to the graph if a matching node is not already
        present.
        """
        if not self.hasNode(id):
            record = Record(name, institution, year, id)
            node = Node(record, ancestors)
            self.nodes[id] = node
            if self.head is None:
                self.head = node
        else:
            msg = "node with id %d already exists" % (id)
            raise DuplicateNodeError(msg)

    def generateDotFile(self):
        """
        Return a string that contains the content of the Graphviz dotfile
        format for this graph.
        """
        if self.head is None:
            return ""

        queue = [self.head.id()]
        edges = ""
        dotfile = ""
        
        dotfile += """digraph genealogy {
    graph [charset="utf-8"];
    node [shape=plaintext];
    edge [style=bold];\n\n"""

        while len(queue) > 0:
            node_id = queue.pop()
            node = self.getNode(node_id)

            if node.already_printed:
                continue
            else:
                node.already_printed = True
            
            # Add this node's advisors to queue.
            queue += node.ancestors
        
            # Print this node's information.
            nodestr = "    %d [label=\"%s\"];" % (node_id, node)
            dotfile += nodestr

            # Store the connection information for this node.
            for advisor in node.ancestors:
                edgestr = "\n    %s -> %d;" % (advisor, node_id)
                edges += edgestr
                
            dotfile += "\n"

        # Now print the connections between the nodes.
        dotfile += edges

        dotfile += "\n}\n"
        return dotfile
