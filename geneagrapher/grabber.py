import urllib
import re
from BeautifulSoup import BeautifulSoup

class Grabber:
    """
    Class for grabbing and parsing mathematician information from
    Math Genealogy Database.
    """
    def __init__(self, id):
        self.id = id
        self.name = None
        self.institution = None
        self.year = None
        self.advisors = []
        self.descendants = []

    def get_page(self):
        """
        Grab the page for self.id from the Math Genealogy Database.
        """
        url = 'http://genealogy.math.ndsu.nodak.edu/id.php?id=' + str(self.id)
        return urllib.urlopen(url)
            
    def extract_node_information(self):
        """
        For the mathematician in this object, extract the list of
        advisor ids, the mathematician name, the mathematician
        institution, and the year of the mathematician's degree.
        """
        page = self.get_page()
        soup = BeautifulSoup(page, convertEntities='html')
        page.close()
            
        self.advisors = []
        self.descendants = []

        if soup.firstText().text == u"You have specified an ID that does not exist in the database. Please back up and try again.":
            # Then a bad URL (e.g., a bad record id) was given. Throw an exception.
            msg = "Invalid page address for id {}".format(self.id)
            raise ValueError(msg)

        # Get mathematician name.
        self.name = soup.find('h2').getText()

        # Get institution name (or None, if it there is no institution name).
        self.institution = soup.find('div', style="line-height: 30px; text-align: center; margin-bottom: 1ex").find('span').find('span').text
        if self.institution == u'':
            self.institution = None

        # Get graduation year, if present.
        inst_year = soup.find('div', style="line-height: 30px; text-align: center; margin-bottom: 1ex").find('span').contents[-1].strip()
        if inst_year.isdigit():
            self.year = int(inst_year)

        # Get advisor IDs.
        for advisor_info in soup.findAll(text=re.compile('Advisor')):
            if 'Advisor: Unknown' not in advisor_info:
                advisor_id = advisor_info.findNext().attrs[0][-1].split('=')[1]
                self.advisors.append(int(advisor_id))

        # Get descendant IDs.
        if soup.find('table') is not None:
            for descendant_info in soup.find('table').findAll('a'):
                descendant_id = descendant_info.attrs[0][-1].split('=')[-1]
                self.descendants.append(int(descendant_id))
        return [self.name, self.institution, self.year, self.advisors, self.descendants]
