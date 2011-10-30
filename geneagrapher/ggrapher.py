import geneagrapher

def ggrapher():
    """Function to run the Geneagrapher. This is the function called when
    the ggrapher script is run."""
    ggrapher = geneagrapher.Geneagrapher()
    try:
        ggrapher.parse_input()
    except SyntaxError, e:
        print ggrapher.parser.get_usage()
        print e
    ggrapher.build_graph()
    ggrapher.generate_dot_file()
