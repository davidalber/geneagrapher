from optparse import OptionParser
import GGraph
import grab

class Geneagrapher:
	"""
	A class for building Graphviz "dot" files for math genealogies
	extracted from the Mathematics Genealogy Project website.
	"""
	def __init__(self):
		self.graph = GGraph.Graph()
		self.leaf_ids = []
		self.get_ancestors = True
		self.get_descendents = False
		self.verbose = False
		self.write_filename = None

	def parseInput(self):
		"""
		Parse command-line information.
		"""
		self.parser = OptionParser()

		self.parser.set_usage("%prog [options] ID ...")
		self.parser.set_description('Create a Graphviz "dot" file for a mathematics genealogy, where ID is a record identifier from the Mathematics Genealogy Project. Multiple IDs may be passed.')

		self.parser.add_option("-f", "--file", dest="filename",
				       help="write report to FILE [default: stdout]", metavar="FILE", default=None)
		self.parser.add_option("--without-ancestors", action="store_false", dest="get_ancestors",
				       default=True, help="do not get ancestors of any input IDs")
		self.parser.add_option("--with-descendents", action="store_true", dest="get_descendents",
				       default=False, help="do not get ancestors of any input IDs")
		self.parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
				       help="print information showing progress")
		self.parser.add_option("--version", "-V", action="store_true", dest="print_version", default=False,
				       help="print geneagrapher version and exit")

		(options, args) = self.parser.parse_args()
		
		if options.print_version:
			print "Geneagrapher Version 0.2"
			self.parser.exit()
		
		if len(args) == 0:
			raise SyntaxError("%s: error: no record IDs passed" % (self.parser.get_prog_name()))

		self.get_ancestors = options.get_ancestors
		self.get_descendents = options.get_descendents
		self.verbose = options.verbose
		self.write_filename = options.filename
		for arg in args:
			self.leaf_ids.append(int(arg))
		
	def buildGraph(self):
		"""
		Populate the graph member by grabbing the mathematician
		pages and extracting relevant data.
		"""
		grab_queue = list(self.leaf_ids)
		while len(grab_queue) != 0:
			id = grab_queue.pop()
			if not self.graph.hasNode(id):
				# Then this information has not yet been grabbed.
				grabber = grab.Grabber(id)
				if self.verbose:
					print "Grabbing record #%d" % (id)
				try:
					[name, institution, year, advisors] = grabber.extractNodeInformation()
				except ValueError:
					# The given id does not exist in the Math Genealogy Project's database.
					raise
				if id in self.leaf_ids:
					self.graph.addNode(name, institution, year, id, advisors, True)
				else:
					self.graph.addNode(name, institution, year, id, advisors)
				if self.get_ancestors:
					grab_queue += advisors
					
	def generateDotFile(self):
		dotfile = self.graph.generateDotFile()
		if self.write_filename is not None:
			outfile = open(self.write_filename, "w")
			outfile.write(dotfile)
			outfile.close()
		else:
			print dotfile
		
if __name__ == "__main__":
	geneagrapher = Geneagrapher()
	try:
		geneagrapher.parseInput()
	except SyntaxError, e:
		print geneagrapher.parser.get_usage()
		print e
	geneagrapher.buildGraph()
	geneagrapher.generateDotFile()
