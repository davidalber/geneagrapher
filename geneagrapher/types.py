from typing import (
    Dict,
    List,
    Literal,
    NewType,
    Optional,
    TypedDict,
)

# RecordId, Record, and Geneagraph mirror types of the same name in
# geneagrapher-core.
RecordId = NewType("RecordId", int)


class Record(TypedDict):
    id: RecordId
    name: str
    institution: Optional[str]
    year: Optional[int]
    descendants: List[int]
    advisors: List[int]


class Geneagraph(TypedDict):
    start_nodes: List[RecordId]
    nodes: Dict[RecordId, Record]
    status: Literal["complete", "truncated"]
