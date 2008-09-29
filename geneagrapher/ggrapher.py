import geneagrapher

def ggrapher():
	ggrapher = geneagrapher.Geneagrapher()
	try:
		ggrapher.parseInput()
	except SyntaxError, e:
		print ggrapher.parser.get_usage()
		print e
	ggrapher.buildGraph()
	ggrapher.generateDotFile()
