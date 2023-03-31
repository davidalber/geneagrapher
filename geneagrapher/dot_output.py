from .types import Record

from typing import Generator


def make_node_str(record: Record) -> str:
    label = record["name"]
    institution = record["institution"]
    year = record["year"]
    if institution is not None or year is not None:
        inst_comp = [institution] if institution is not None else []
        year_comp = [f"({year})"] if year is not None else []
        label += "\\n" + " ".join(inst_comp + year_comp)

    return f'{record["id"]} [label="{label}"];'


def make_edge_str(record: Record) -> Generator[str, None, None]:
    for advisor in set(
        record["advisors"]
    ):  # using `set` to eliminate the occasional duplicate advisor (e.g., at this
        # time, 125886)
        yield f'{advisor} -> {record["id"]};'
