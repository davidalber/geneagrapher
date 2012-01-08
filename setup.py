from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '1.0c2'

install_requires = [
    'BeautifulSoup >= 3.2.0'
]


setup(name='geneagrapher',
    version=version,
    description="Generates mathematic genealogy graph files.",
    long_description=README + '\n\n' + NEWS,
    classifiers=[
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
    keywords='',
    author='David Alber',
    author_email='alber.david@gmail.com',
    url='http://www.davidalber.net/geneagrapher',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['ggrapher=geneagrapher.geneagrapher:ggrapher']
    },
    test_suite='tests.geneagrapher'
)
