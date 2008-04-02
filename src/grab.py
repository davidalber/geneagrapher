import urllib
from GGraph import *

#id = 7401

def extractNodeInformation(id, graph):
    search_list = [id]

    while len(search_list) > 0:
        id = search_list.pop()
        #url = 'http://genealogy.math.ndsu.nodak.edu/html/id.phtml?id=' + str(id)
        url = 'http://genealogy.math.ndsu.nodak.edu/id.php?id=' + str(id)
        #url = 'http://www.genealogy.ams.org/html/id.phtml?id=' + str(id)
        page = urllib.urlopen(url)

        advisors = []
        name = ''
        institution = ''
        year = -1

        line = page.readline()
        if line.find("<html>An error occurred in the forwarding block") > -1:
            # Then a bad URL was given. Throw an exception.
            raise ValueError("Invalid address given: " + url)


        while line != '':
            line = page.readline()
            line = line.decode('utf-8')
            if line.find('h2 style=') > -1:
            	line = page.readline()
            	line = line.decode('utf-8')
                name = line.split('</h2>')[0].strip()

            if line.find('#006633; margin-left: 0.5em">') > -1:
                inst_year = line.split('#006633; margin-left: 0.5em">')[1].split("</span>")[:2]
                institution = inst_year[0].strip()
                if inst_year[1].strip().isdigit():
                    year = int(inst_year[1].strip())

            if line.find('Advisor') > -1:
                if line.find('a href=\"id.php?id=') > -1:
                    # Extract link to advisor page.
                    advisor_id = int(line.split('a href=\"id.php?id=')[1].split('\">')[0])
                    advisors.append(advisor_id)
                    if not graph.hasNode(advisor_id) and search_list.count(advisor_id) == 0:
                        search_list.append(advisor_id)
            elif line.find('Student(s)') > -1 or line.find('No students known') > -1:
                break

        #    print name.encode('iso-8859-1', 'replace')
        #    print institution.encode('iso-8859-1', 'replace'), year
        #    print advisors

        if not graph.hasNode(id):
            # Add node to graph.
            graph.addNode(name, institution, year, id, advisors)
