from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="Geneagrapher",
      version="0.2",
      description="Generates mathematic genealogy graph files.",
      long_description="""\
The Geneagrapher generates Graphviz "dot" files of mathematical
genealogies using data from the Math Genealogy Project's website.
""",
      author="David Alber",
      author_email="alber.david@gmail.com",
      url="http://www.davidalber.net/",
      packages=find_packages(exclude='tests'),
      #package_data={'': '*.xml'},
      install_requires=[],
      scripts=['geneagrapher/ggrapher.py'],
      test_suite = "tests.tests"
      )

