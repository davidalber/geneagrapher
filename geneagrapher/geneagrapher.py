from argparse import ArgumentParser
from collections import deque
from importlib.metadata import PackageNotFoundError, version
import pkg_resources
import sys




if __name__ == "__main__":
    description = 'Create a Graphviz "dot" file for a mathematics \
genealogy, where ID is a record identifier from the Mathematics Genealogy \
Project. Multiple IDs may be passed.'
    parser = ArgumentParser(description=description)

    try:
        pkg_version = version("geneagrapher")
    except PackageNotFoundError:
        pkg_version = "dev"
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {pkg_version}"
    )
    parser.add_argument(
        "-o",
        "--out",
        dest="filename",
        help="write output to FILE [default: stdout]",
        metavar="FILE",
        default=sys.stdout,
    )
    parser.add_argument("-ta", "--traverse-advisors", nargs="+", type=int, metavar="ID", default=[])
    parser.add_argument(
        "-a",
        "--with-ancestors",
        action="store_true",
        dest="get_ancestors",
        default=False,
        help="retrieve ancestors of IDs and include in graph",
    )
    parser.add_argument(
        "-d",
        "--with-descendants",
        action="store_true",
        dest="get_descendants",
        default=False,
        help="retrieve descendants of IDs and include in graph",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="do not display the progress bar",
    )
    parser.add_argument(
        "ids", metavar="ID", type=RecordIdArg, nargs="+", help="mathematician record ID"
    )

    args = parser.parse_args()
    print(args)
