from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="Geneagrapher",
      version="0.2.1-r2",
      description="Generates mathematic genealogy graph files.",
      long_description="""\
The Geneagrapher generates Graphviz "dot" files of mathematical
genealogies using data from the Math Genealogy Project's website.
""",
      author="David Alber",
      author_email="alber.david@gmail.com",
      url="http://www.davidalber.net/",
      license="MIT",
      packages=find_packages(exclude='tests'),
      install_requires=[],
      entry_points = {
        'console_scripts': [
            'ggrapher = geneagrapher.geneagrapher:ggrapher'
        ]
      },
      test_suite = "tests.tests"
)

