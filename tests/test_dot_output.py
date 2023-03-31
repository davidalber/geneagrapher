from geneagrapher.dot_output import make_edge_str, make_node_str
from geneagrapher.types import Record, RecordId

from itertools import zip_longest
import pytest
from typing import List


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
