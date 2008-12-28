import urllib
import re
from htmlentitydefs import name2codepoint

class BadIdError(ValueError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Grabber:
    """
    Class for grabbing and parsing mathematician information from
    Math Genealogy Database.
    """
    def __init__(self, id):
        self.id = id
        self.pagestr = None
        self.name = None
        self.institution = None
        self.year = None
        self.advisors = []
        self.descendants = []

    def unescape(self, s):
        return re.sub('&(%s);' % '|'.join(name2codepoint),\
                      lambda m: unichr(name2codepoint[m.group(1)]), s)

    def getPage(self):
        """
        Grab the page for self.id from the Math Genealogy Database.
        """
        if self.pagestr is None:
            url = 'http://genealogy.math.ndsu.nodak.edu/id.php?id=' + str(self.id)
            page = urllib.urlopen(url)
            self.pagestr = page.read()
            self.pagestr = self.pagestr.decode('utf-8')
            
    def extractNodeInformation(self):
        """
        For the mathematician in this object, extract the list of
        advisor ids, the mathematician name, the mathematician
        institution, and the year of the mathematician's degree.
        """
        if self.pagestr is None:
            self.getPage()
            
        self.advisors = []
        self.descendants = []

        # Split the page string at newline characters.
        psarray = self.pagestr.split('\n')
        
        if psarray[0].find("An error occurred in the forwarding block") > -1 or \
                psarray[0].find("DB Error: invalid number") > -1:
            # Then a bad URL (e.g., a bad record id) was given. Throw an exception.
            msg = "Invalid page address for id %d" % (self.id)
            raise BadIdError(msg)

        lines = iter(psarray)
        for line in lines:
            if line.find('h2 style=') > -1:
                line = lines.next()
                self.name = self.unescape(line.split('</h2>')[0].strip())

            if '#006633; margin-left: 0.5em">' in line:
                inst_year = line.split('#006633; margin-left: 0.5em">')[1].split("</span>")[:2]
                self.institution = self.unescape(inst_year[0].strip())
                if self.institution == u"":
                    self.institution = None
                if inst_year[1].split(',')[0].strip().isdigit():
                    self.year = int(inst_year[1].split(',')[0].strip())

            if 'Advisor' in line:
                if 'a href=\"id.php?id=' in line:
                    # Extract link to advisor page.
                    advisor_id = int(line.split('a href=\"id.php?id=')[1].split('\">')[0])
                    self.advisors.append(advisor_id)

            if '<tr ' in line:
                descendant_id = int(line.split('a href=\"id.php?id=')[1].split('\">')[0])
                self.descendants.append(descendant_id)
                
            if 'According to our current on-line database' in line:
                break
        return [self.name, self.institution, self.year, self.advisors, self.descendants]
