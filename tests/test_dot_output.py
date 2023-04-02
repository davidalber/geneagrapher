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
    "record,graph_nodes,expected",
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
            [1000],
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
            [1000, 1001, 1002, 1003],
            ["1001 -> 1000;", "1002 -> 1000;", "1003 -> 1000;"],
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
            [1000, 1001, 1002],
            ["1001 -> 1000;", "1002 -> 1000;"],
        ],
    ),
)
def test_make_edge_str(
    record: Record, graph_nodes: List[int], expected: List[str]
) -> None:
    graph: Geneagraph = {
        "start_nodes": s.start_nodes,
        "nodes": {RecordId(aid): s.rec for aid in graph_nodes},
        "status": s.status,
    }
    for edge_str, expected_edge_str in zip_longest(
        make_edge_str(record, graph), expected
    ):
        assert edge_str == expected_edge_str


class TestDotOutput:
    def test_init(self) -> None:
        do = DotOutput(s.graph)
        assert do.graph == s.graph

    @patch(
        "geneagrapher.dot_output.make_edge_str",
        side_effect=[
            iter(["edge1"]),
            iter(["edge2"]),
            iter(["edge3"]),
            iter(["edge4"]),
        ],
    )
    @patch(
        "geneagrapher.dot_output.make_node_str",
        side_effect=["node1", "node2", "node3", "node4"],
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
                    "advisors": [999],
                },
                RecordId(999): {
                    "id": RecordId(999),
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
                    "advisors": [1003],
                },
                RecordId(1003): {
                    "id": RecordId(1002),
                    "name": "A Fourth Name",
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
    graph [ordering="out"];
    node [shape=plaintext];
    edge [style=bold];

    {nodes}

    {edges}
}}""".format(
                nodes="\n    ".join(["node1", "node2", "node3", "node4"]),
                edges="\n    ".join(["edge1", "edge2", "edge3", "edge4"]),
            )
        )

        assert m_make_node_str.call_args_list == [
            call(graph["nodes"][RecordId(999)]),
            call(graph["nodes"][RecordId(1000)]),
            call(graph["nodes"][RecordId(1002)]),
            call(graph["nodes"][RecordId(1003)]),
        ]
        assert m_make_edge_str.call_args_list == [
            call(graph["nodes"][RecordId(999)], graph),
            call(graph["nodes"][RecordId(1003)], graph),
            call(graph["nodes"][RecordId(1002)], graph),
            call(graph["nodes"][RecordId(1000)], graph),
        ]
