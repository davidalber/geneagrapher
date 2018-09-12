import os
import sys
from bs4 import BeautifulSoup
from geneagrapher.grabber import get_record_from_tree


class LocalDataGrabber:
    """A class for grabbing locally-cached test data."""
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    @classmethod
    def data_file(cls, filename):
        """Return the absolute path to the data file with given name."""
        return os.path.join(cls.data_path, filename)

    def get_record(self, id):
        """Load the local data for the given id and use Grabber's functionas
        to extract the record data."""
        with open(self.data_file('{0}.html'.format(id)), 'r') as fin:
            soup = BeautifulSoup(fin, 'lxml')
        return get_record_from_tree(soup, id)


file_path = os.path.abspath(__file__)
LocalDataGrabber.data_path = os.path.join(os.path.dirname(file_path),
                                          'testdata')
