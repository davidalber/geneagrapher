import urllib
import re
from BeautifulSoup import BeautifulSoup


class Grabber:
    """
    Class for grabbing and parsing mathematician information from
    Math Genealogy Database.
    """
    def __init__(self, **kwargs):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def get_record(self, id):
        """
        For the mathematician in this object, extract the list of
        advisor ids, the mathematician name, the mathematician
        institution, and the year of the mathematician's degree.
        """
        url = 'http://genealogy.math.ndsu.nodak.edu/id.php?id=' + str(id)
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, convertEntities='html')
        page.close()

        if soup.firstText().text == u"You have specified an ID that does not \
exist in the database. Please back up and try again.":
            # Then a bad URL (e.g., a bad record id) was given. Throw an
            # exception.
            msg = "Invalid id {}".format(id)
            raise ValueError(msg)

        # Get mathematician name.
        name = soup.find('h2').getText()

        # Get institution name (or None, if it there is no institution name).
        institution = soup.find('div', style="line-height: 30px; \
text-align: center; margin-bottom: 1ex").find('span').find('span').text
        if institution == u'':
            institution = None

        # Get graduation year, if present.
        inst_year = soup.find('div', style="line-height: 30px; text-align: \
center; margin-bottom: 1ex").find('span').contents[-1].strip()
        if inst_year.isdigit():
            year = int(inst_year)
        else:
            year = None

        # Get advisor IDs.
        advisors = set([extract_id(info.findNext()) for info in
                             soup.findAll(text=re.compile('Advisor'))
                             if 'Advisor: Unknown' not in info])

        # Get descendant IDs.
        if soup.find('table') is not None:
            descendants = set([extract_id(info) for info in
                                    soup.find('table').findAll('a')])
        else:
            descendants = set([])

        return [name, institution, year, advisors, descendants]


def extract_id(tag):
    """Extract the ID from a tag with form <a href="id.php?id=7401">."""
    return int(tag.attrs[0][-1].split('=')[-1])
