# 1.0.0
Released 07-Oct-2018

- Redesigned data-grabbing interface to allow for the introduction of
  new data grabbers.
- Added a new data grabber that builds a local cache of records. This
  allows subsequent geneagrapher calls to obtain cached records and
  avoiding a request over the network.
- Added local test data, allowing for many tests that were previously
  making network requests to simply load local data. This speeds up
  running the test suite substantially.
- Substantial refactoring and internal changes, including:
  - Better code coverage by the tests.
  - Updated packaging to more modern standards.
  - Improved test documentation and naming.
  - Internal graph structure now only stores the genealogy
    graph. Previously, the graph structure retained all edges from the
    Math Genealogy Project information.
  - Data is now extracted from Math Genealogy Project web pages using
    [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/). This
    means that the Geneagrapher now has an external dependency, but I
    believe the advantages for testing and code readability, for this
    case, outweigh the disadvantage of taking a dependency.

# 0.2.1-r2
Released 11-Aug-2011

- A test in Geneagrapher 0.2.1-r1 was broken by new information
  addedto the Mathematics Genealogy Project. This release fixes the
  test, but does not change the functionality from version 0.2.1-r1.

# 0.2.1-r1
Released 03-Nov-2010

- A few tests in Geneagrapher 0.2.1 have become broken since that
  version was released. This release fixes those tests, but does not
  change the functionality from version 0.2.1.

# 0.2.1
Released 01-Sep-2009

- Multiple advisors are now captured correctly. While this problem was
  manifesting itself, ancestor trees were coming out as a branch-free
  tree.
- Added a test for the multiple advisor case, which enables quicker
  recognition of similar problems.
- Updated a few tests that had become broken due to updates in the
  Math Genealogy Project’s database.


# 0.2-r1
Released 07-Oct-2008

- This Geneagrapher release slightly changes an installation-related
  file to enable installation on machines running Python 2.6 that have
  not yet installed Python setuptools.

# 0.2.0
Released 06-Oct-2008

Here are the most significant changes, from the perspective of the
user:

- Descendant trees. Now trees can be built placing a starting node at
  the top and graphing all of its descendants. A couple points on
  this:
  - These sorts of graphs tend to have a lot of “fan out” because some
    people have a lot of students.
  - Be careful. Do not inadvertently (or intentionally!) run a job that
    requests the data for thousands of nodes.
- Better character handling. I believe all characters are now
  displayed correctly, as long as the generated dot file is processed
  by Graphviz a certain way (see the Geneagrapher 0.2 Usage Guide).
- No limit on the number of starting nodes.
- This is a client application, meaning the user installs it somewhere
  and runs it there. Furthermore, this package only generates the
  input file to Graphviz, so that also needs to be installed. This is
  probably more of a hassle than most Geneagrapher users want to go
  through (not all, though), but this is just the first step.

Additionally, behind-the-scenes changes happened:

- Large portions of the code were rewritten.
- Added a test suite to make it more maintainable. In particular, this
  should allow quicker diagnosis and modifications when the
  Mathematics Genealogy Project pages have changed.
