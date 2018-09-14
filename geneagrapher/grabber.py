import urllib
import re
from bs4 import BeautifulSoup


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
        url = "http://genealogy.math.ndsu.nodak.edu/id.php?id=" + str(id)
        page = urllib.urlopen(url)
        soup = BeautifulSoup(page, "lxml")
        page.close()

        return get_record_from_tree(soup, id)


def get_record_from_tree(soup, id):
    """Extract and return the fields in the mathematician record using the
    input tree."""
    if not has_record(soup):
        # Then a bad record id was given. Raise an exception.
        msg = "Invalid id {}".format(id)
        raise ValueError(msg)

    record = {}
    record["name"] = get_name(soup)
    record["institution"] = get_institution(soup)
    record["year"] = get_year(soup)
    record["advisors"] = get_advisors(soup)
    record["descendants"] = get_descendants(soup)
    return record


def has_record(soup):
    """Return True if the input tree contains a mathematician record and False
    otherwise."""
    if soup.p.string == "Non-numeric id supplied. Aborting.":
        # This is received, for instance, by going to
        # http://genealogy.math.ndsu.nodak.edu/id.php?id=999999999999999999999.
        return False
    return (
        not soup.p.string
        == u"You have specified an ID that does \
not exist in the database. Please back up and try again."
    )


def get_name(soup):
    """Extract the name from the given tree."""
    try:
        name = soup.find("h2").getText(strip=True)
    except AttributeError:
        name = ""
    return name


def get_institution(soup):
    """Return institution name (or None, if there is no institution name)."""
    try:
        institution = (
            soup.find(
                "div",
                style="line-height: 30px; \
text-align: center; margin-bottom: 1ex",
            )
            .find("span")
            .find("span")
            .text
        )
        if institution == u"":
            institution = None
    except AttributeError:
        institution = None
    return institution


def get_year(soup):
    """Return graduation year (or None, if there is no graduation year)."""
    try:
        inst_year = (
            soup.find(
                "div",
                style="line-height: 30px; text-align: \
center; margin-bottom: 1ex",
            )
            .find("span")
            .contents[-1]
            .strip()
        )
        if inst_year.isdigit():
            return int(inst_year)
        else:
            return None
    except AttributeError:
        return None


def get_advisors(soup):
    """Return the set of advisors."""
    return set(
        [
            extract_id(info.findNext())
            for info in soup.findAll(text=re.compile("Advisor"))
            if "Advisor: Unknown" not in info
        ]
    )


def get_descendants(soup):
    """Return the set of descendants."""
    if soup.find("table") is not None:
        return set([extract_id(info) for info in soup.find("table").findAll("a")])
    else:
        return set([])


def extract_id(tag):
    """Extract the ID from a tag with form <a href="id.php?id=7401">."""
    return int(tag.attrs["href"].split("=")[-1])
