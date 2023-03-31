from geneagrapher.dot_output import DotOutput, make_edge_str, make_node_str
from geneagrapher.types import Geneagraph, Record, RecordId

from itertools import zip_longest
import pytest
from typing import List
from unittest.mock import MagicMock, call, patch, sentinel as s


@pytest.mark.parametrize(
    "record,expected",
    (
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": "The Institution",
                "year": 1900,
                "descendants": [],
                "advisors": [],
            },
            r'1000 [label="The Name\nThe Institution (1900)"];',
        ],
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": "The Institution",
                "year": None,
                "descendants": [],
                "advisors": [],
            },
            r'1000 [label="The Name\nThe Institution"];',
        ],
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": None,
                "year": 1900,
                "descendants": [],
                "advisors": [],
            },
            r'1000 [label="The Name\n(1900)"];',
        ],
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": None,
                "year": None,
                "descendants": [],
                "advisors": [],
            },
            '1000 [label="The Name"];',
        ],
    ),
)
def test_make_node_str(record: Record, expected: str) -> None:
    assert make_node_str(record) == expected


@pytest.mark.parametrize(
    "record,expected",
    (
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": None,
                "year": None,
                "descendants": [],
                "advisors": [],
            },
            [],
        ],
        [
            {
                "id": RecordId(1000),
                "name": "The Name",
                "institution": None,
                "year": None,
                "descendants": [],
                "advisors": [1001, 1002, 1003],
            },
            ["1001 -> 1000;", "1002 -> 1000;", "1003 -> 1000;"],
        ],
    ),
)
def test_make_edge_str(record: Record, expected: List[str]) -> None:
    for edge_str, expected_edge_str in zip_longest(make_edge_str(record), expected):
        assert edge_str == expected_edge_str


class TestDotOutput:
    def test_init(self) -> None:
        do = DotOutput(s.graph)
        assert do.graph == s.graph

    @patch(
        "geneagrapher.dot_output.make_edge_str",
        side_effect=[iter(["edge1"]), iter(["edge2"]), iter(["edge3"])],
    )
    @patch(
        "geneagrapher.dot_output.make_node_str", side_effect=["node1", "node2", "node3"]
    )
    def test_output(
        self, m_make_node_str: MagicMock, m_make_edge_str: MagicMock
    ) -> None:
        graph: Geneagraph = {
            "start_nodes": [],
            "nodes": {
                RecordId(1000): {
                    "id": RecordId(1000),
                    "name": "The Name",
                    "institution": "The Institution",
                    "year": 1900,
                    "descendants": [],
                    "advisors": [1001],
                },
                RecordId(1001): {
                    "id": RecordId(1001),
                    "name": "The Second Name",
                    "institution": "The Second Institution",
                    "year": None,
                    "descendants": [],
                    "advisors": [1002],
                },
                RecordId(1002): {
                    "id": RecordId(1002),
                    "name": "The Third Name",
                    "institution": None,
                    "year": 1800,
                    "descendants": [],
                    "advisors": [],
                },
            },
            "status": "complete",
        }

        do = DotOutput(graph)
        assert (
            do.output
            == """digraph {{
    node [shape=plaintext];
    edge [style=bold];

    {nodes}

    {edges}
}}""".format(
                nodes="\n    ".join(["node1", "node2", "node3"]),
                edges="\n    ".join(["edge1", "edge2", "edge3"]),
            )
        )

        assert m_make_node_str.call_args_list == [
            call(graph["nodes"][RecordId(1000)]),
            call(graph["nodes"][RecordId(1001)]),
            call(graph["nodes"][RecordId(1002)]),
        ]
        assert m_make_edge_str.call_args_list == [
            call(graph["nodes"][RecordId(1000)]),
            call(graph["nodes"][RecordId(1001)]),
            call(graph["nodes"][RecordId(1002)]),
        ]
