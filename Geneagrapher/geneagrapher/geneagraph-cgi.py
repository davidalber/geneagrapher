#!/usr/bin/python

import cgi
import random
import os
import time
from grab import *
from GGraph import *
#import cgitb; cgitb.enable() # for debugging, comment out for production

form = cgi.FieldStorage()
name = form.getfirst("name", "")
extra = form.getfirst("extra", "")
nodes = form.getlist("node")
output = form.getfirst("output", "png")

# Save the input to log file.
f = open("/var/log/geneagraph", "a")
f.write(time.strftime('%m/%d/%Y %H:%M:%S'))
f.write(" ")
f.write(os.environ['REMOTE_ADDR'])
f.write("\n")
if name != "":
	f.write("\tName: ")
	f.write(name)
	f.write("\n")
if extra != "":
	f.write("\tExtra: ")
	f.write(extra)
	f.write("\n")
if len(nodes) > 0:
	f.write("\t")
	f.write(str(nodes))
	f.write("\n")
f.close()

try:
	if len(name) > 100:
		raise ValueError("Name field longer than maximum allowed length (100 characters).")
	if len(extra) > 100:
		raise ValueError("Extra field longer than maximum allowed length (100 characters).")
	if len(nodes) > 5:
	#if len(nodes) > 50:
		raise ValueError("Only five node URLs may be supplied.")

# Replace special characters in name and extra with backslashed form
	name = name.replace('\\', '\\\\')
	name = name.replace('\"', '\\"')
	extra = extra.replace('\\', '\\\\')
	extra = extra.replace('"', '\\"')

	record = Record(name, extra, -1, 0)

	printHead = True
	if name == "" and extra == "":
		printHead = False

	advisors = []
	for index in range(len(nodes)):
		if not nodes[index].isspace():
			if nodes[index].find('id.php?id=') > -1:
				id = nodes[index].split('id.php?id=')[1].strip()
				if id.isdigit():
					advisors.append(int(id))
				else:
					raise ValueError("Node " + str(index+1) + " was improperly formatted.")
			else:
				raise ValueError("Node " + str(index+1) + " was improperly formatted.")

		
	node = Node(record, advisors)
	graph = Graph(node, printHead)

	for advisor in advisors:
		extractNodeInformation(advisor, graph)

	fnum = str(int(random.random()*1000000000000000))
	filename = '/tmp/' + fnum + '.dot'
	graph.writeDotFile(filename)

	if output == "dot":
		print "Content-Type: text/html"
		print
		print "<html><body><pre>"
		f = open(filename, "r")
		file = f.read()
		f.close()
		print file
		print "</pre></body></html>"
	elif output == "png" or output == "ps":
		psfilename = '/tmp/' + fnum + '.ps'
		command = '/usr/local/bin/dot -Tps ' + filename + ' -o ' + psfilename
		os.system(command)
		if output == "png":
			pngfilename = '/tmp/' + fnum + '.png'
			command = '/usr/bin/convert -density 144 -geometry 50% ' + psfilename + ' ' + pngfilename
			os.system(command)
			print "Content-type: image/png"
			print "Content-Disposition: attachment; filename=genealogy.png"
			print
			f = open(pngfilename, "r")
		elif output == "ps":
			print "Content-Type: application/postscript"
			print
			f = open(psfilename, "r")
		file = f.read()
		f.close()
		print file
	else: # improper output chosen
		raise ValueError("Return type was improperly formatted. Go back and check it out.")

	command = '/bin/rm /tmp/' + fnum + '.*'
	os.system(command)

except ValueError, e:
	print "Content-type: text/html"
	print
	print e, "<br>Go back and check it out."
	raise SystemExit
