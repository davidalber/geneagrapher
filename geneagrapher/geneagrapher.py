from argparse import ArgumentParser
from importlib.metadata import PackageNotFoundError, version
import re
import sys


class RecordIdArg:
    def __init__(self, val):
        # Validate the input.
        match = re.fullmatch("(\d+)(?::(a|d|ad|da))?", val)
        if match is None:
            raise ValueError()
        self.record_id = int(match.group(1))
        self.request_advisors = "a" in (match.group(2) or [])
        self.request_descendants = "d" in (match.group(2) or [])


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
    parser.add_argument(
        "-ta", "--traverse-advisors", nargs="+", type=int, metavar="ID", default=[]
    )
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
