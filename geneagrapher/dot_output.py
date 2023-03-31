from .types import Record


def make_node_str(record: Record) -> str:
    label = record["name"]
    institution = record["institution"]
    year = record["year"]
    if institution is not None or year is not None:
        inst_comp = [institution] if institution is not None else []
        year_comp = [f"({year})"] if year is not None else []
        label += "\\n" + " ".join(inst_comp + year_comp)

    return f'{record["id"]} [label="{label}"];'
