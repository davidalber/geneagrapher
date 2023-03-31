from geneagrapher.dot_output import make_node_str
from geneagrapher.types import Record, RecordId

import pytest


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
