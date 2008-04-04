class Record:
    """
    Container class storing record of a mathematician in the graph.
    """
    def __init__(self, name, institution, year, id):
        """
        Construct a Record object.
        
        Parameters:
            name: string containing mathematician's name
            institution: string containing mathematician's instituion (empty if
                none)
            year: integer containing year degree was earned
            id: integer containing Math Genealogy Project id value.
        """
        self.name = name
        self.institution = institution
        self.year = year
        self.id = id
        
        # Verify we got the types wanted.
        if type(self.name) is not type('str'):
            raise TypeError("Unexpected parameter type: expected string value for 'name'")
        if type(self.institution) is not type('str'):
            raise TypeError("Unexpected parameter type: expected string value for 'institution'")
        if type(self.year) is not type(1):
            raise TypeError("Unexpected parameter type: expected integer value for 'year'")
        if type(self.id) is not type(1):
            raise TypeError("Unexpected parameter type: expected integer value for 'id'")

    def __cmp__(self, r2):
        """
        Compare a pair of mathematician records based on ids.
        """
        return self.id.__cmp__(r2.id)
    
    def hasInstitution(self):
        """
        Return True if this record has an institution associated with it, else False.
        """
        return self.institution != ""
    
    def hasYear(self):
        """
        Return True if this record has a year associated with it, else False.
        """
        return self.year != -1
    

class Node:
    "Node in the graph."
    def __init__(self, record, ancestors):
        self.record = record
        self.ancestors = ancestors
        self.already_printed = False

    def __str__(self):
        if self.record.institution != '':
            if self.record.year > -1:
                return self.record.name.encode('iso-8859-1', 'replace') + ' \\n' + self.record.institution.encode('iso-8859-1', 'replace') + ' (' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('iso-8859-1', 'replace') + ' \\n' + self.record.institution.encode('iso-8859-1', 'replace')
        else:
            if self.record.year > -1:
                return self.record.name.encode('iso-8859-1', 'replace') + ' \\n(' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('iso-8859-1', 'replace')

    def __cmp__(self, n2):
        return self.record.__cmp__(n2.record)

    def addAncestor(self, ancestor):
        self.ancestors.append(ancestor)

    def id(self):
        return self.record.id


class Graph:
    def __init__(self, head, displayHead=True):
        self.head = head
        self.nodes = {head.id(): head}
        self.displayHead = displayHead
        
    def hasNode(self, id):
        return self.nodes.has_key(id)

    def getNode(self, id):
        return self.nodes[id]

    def getNodeList(self):
        return self.nodes.keys()

    def addNode(self, name, institution, year, id, ancestors):
        record = Record(name, institution, year, id)
        node = Node(record, ancestors)
        self.nodes[id] = node

    def generateDotFile(self):
        if self.displayHead:
            queue = [self.head.id()]
        else:
            queue = self.head.ancestors
        edges = ""
        dotfile = ""
        
        dotfile += """digraph genealogy {
        graph [charset="iso-8859-1"];
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
            dotfile += "\t" + str(node_id) + " [label=\" " + str(node) + "\"];\n"

            # Store the connection information for this node.
            for advisor in node.ancestors:
                edges += "\n\t" + str(advisor) + " -> " + str(node_id) + ";"

        # Now print the connections between the nodes.
        dotfile += edges

        dotfile += "\n}\n"
        return dotfile

    def printDotFile(self):
        print self.generateDotFile()

    def writeDotFile(self, filename):
        outfile = open(filename, 'w')
        outfile.write(self.generateDotFile())
        outfile.close()
