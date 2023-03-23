from argparse import ArgumentParser
from importlib.metadata import PackageNotFoundError, version
import textwrap
from typing import Dict, List, Literal, TypedDict
import re
import sys


TEXTWRAP_WIDTH = 79


class StartNodeRequest(TypedDict):
    recordId: int
    getAdvisors: bool
    getDescendants: bool


class RequestPayload(TypedDict):
    kind: Literal["build-graph"]
    startNodes: List[StartNodeRequest]


class GgrapherError(Exception):
    def __init__(self, msg: str, *, extra: Dict[str, str] = {}) -> None:
        self.msg = msg
        self.extra = extra

    def __str__(self) -> str:
        ret_arr = [
            textwrap.fill(self.msg, width=TEXTWRAP_WIDTH),
            "",
            textwrap.fill(
                "If this problem persists, please create an issue at \
https://github.com/davidalber/geneagrapher/issues/new, and include the following in \
the issue body:",
                width=TEXTWRAP_WIDTH,
            ),
        ]

        # For the key-value arguments, determine the length of the
        # longest key and use that information to align the columns.
        extras_width = (
            max([len(k) for k in ["Message", "Command"] + list(self.extra.keys())]) + 2
        )  # The 2 is for ": "

        ret_arr.append(f"\n    {'Message:':{extras_width}}{self.msg}")
        ret_arr.append(f"    {'Command:':{extras_width}}{' '.join(sys.argv)}")

        for k, v in self.extra.items():
            key = f"{k}:"
            ret_arr.append(f"    {key:{extras_width}}{v}")

        return "\n".join(ret_arr)


class StartNodeArg:
    def __init__(self, val: str) -> None:
        # Validate the input.
        match = re.fullmatch(r"(\d+)(?::(a|d|ad|da))?", val)
        if match is None:
            raise ValueError()
        self.record_id = int(match.group(1))

        self.request_advisors = "a" in (match.group(2) or [])
        self.request_descendants = "d" in (match.group(2) or [])

        # If no traverse direction was specified, default to advisors.
        if not self.request_advisors and not self.request_descendants:
            self.request_advisors = True

    @property
    def start_node(self) -> StartNodeRequest:
        return {
            "recordId": self.record_id,
            "getAdvisors": self.request_advisors,
            "getDescendants": self.request_descendants,
        }


def make_payload(start_nodes: List[StartNodeArg]) -> RequestPayload:
    return {
        "kind": "build-graph",
        "startNodes": [sn.start_node for sn in start_nodes],
    }


if __name__ == "__main__":
    description = 'Create a Graphviz "dot" file for a mathematics \
genealogy, where ID is a record identifier from the Mathematics Genealogy \
Project.'
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
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="do not display the progress bar",
    )
    parser.add_argument(
        "ids",
        metavar="ID",
        type=StartNodeArg,
        nargs="+",
        help="mathematician record ID; valid formats are 'ID' for advisor traversal, \
'ID:a' for advisor traversal, 'ID:d' for descendant traversal, or 'ID:ad' for advisor \
and descendant traversal",
    )

    args = parser.parse_args()
    print(args)
