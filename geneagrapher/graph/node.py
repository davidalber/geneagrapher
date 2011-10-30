from record import Record

class Node:
    """
    Container class storing a node in the graph.
    """
    def __init__(self, record, ancestors, descendants):
        """
        Node class constructor.
        
        Parameters:
            record: instance of the Record class
            ancestors: list of the record's genealogical ancestors'
                IDs
            descendants: list of this record's genealogical
                descendants' IDs
        """
        
        self.record = record
        self.ancestors = ancestors
        self.descendants = descendants
        self.already_printed = False

        # Verify parameter types.
        if not isinstance(self.record, Record):
            raise TypeError("Unexpected parameter type: expected Record object for 'record'")
        if not isinstance(self.ancestors, list):
            raise TypeError("Unexpected parameter type: expected list object for 'ancestors'")
        if not isinstance(self.descendants, list):
            raise TypeError("Unexpected parameter type: expected list object for 'descendants'")

    def __str__(self):
        if self.record.has_institution():
            if self.record.has_year():
                return self.record.name.encode('utf-8', 'replace') + ' \\n' + self.record.institution.encode('utf-8', 'replace') + ' (' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('utf-8', 'replace') + ' \\n' + self.record.institution.encode('utf-8', 'replace')
        else:
            if self.record.has_year():
                return self.record.name.encode('utf-8', 'replace') + ' \\n(' + str(self.record.year) + ')'
            else:
                return self.record.name.encode('utf-8', 'replace')

    def __cmp__(self, n2):
        return self.record.__cmp__(n2.record)

    def add_ancestor(self, ancestor):  # NOTE: is this used?
        """
        Append an ancestor id to the ancestor list.
        """
        # Verify we were passed an int.
        if not isinstance(ancestor, int):
            raise TypeError("Unexpected parameter type: expected int for 'ancestor'")
        self.ancestors.append(ancestor)

    def get_id(self):
        """
        Accessor method to retrieve the id of this node's record.
        """
        return self.record.id

    def set_id(self, id):
        """
        Sets the record id.
        """
        self.record.id = id
