import sys
import geneagrapher

def ggrapher():
	"""Function to run the Geneagrapher. This is the function called when
	the ggrapher script is run."""
	ggrapher = geneagrapher.Geneagrapher()
	try:
		ggrapher.parseInput()
	except SyntaxError, e:
		print ggrapher.parser.get_usage()
		print e
		sys.exit()
	except geneagrapher.BadSortTypeError, msg:
		print msg
		sys.exit()
	ggrapher.buildGraph()
	ggrapher.generateDotFile()
