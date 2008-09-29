from geneagrapher import *

def ggrapher():
	geneagrapher = Geneagrapher()
	try:
		geneagrapher.parseInput()
	except SyntaxError, e:
		print geneagrapher.parser.get_usage()
		print e
	geneagrapher.buildGraph()
	geneagrapher.generateDotFile()
