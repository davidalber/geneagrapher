from geneagrapher.geneagrapher import StartNodeArg, StartNodeRequest, make_payload

import pytest
from typing import List


class TestStartNodeArg:
    @pytest.mark.parametrize(
        "record_id,record_id_valid",
        (
            ["10", True],
            ["3829", True],
            ["10a", False],
            ["a10", False],
            ["blue", False],
        ),
    )
    @pytest.mark.parametrize(
        "aux_config,aux_config_valid",
        (
            ["", True],
            [":a", True],
            [":d", True],
            [":ad", True],
            [":da", True],
            ["a", False],
            [":ab", False],
            [":abd", False],
            [":b", False],
            [":A", False],
            [":D", False],
            [":Ad", False],
        ),
    )
    def test_init(
        self,
        record_id: str,
        record_id_valid: bool,
        aux_config: str,
        aux_config_valid: bool,
    ) -> None:
        if record_id_valid and aux_config_valid:
            rid = StartNodeArg(record_id + aux_config)
            assert rid.record_id == int(record_id)
            assert rid.request_advisors is (
                ("a" in aux_config) or ("a" not in aux_config and "d" not in aux_config)
            )
            assert rid.request_descendants is ("d" in aux_config)
        else:
            with pytest.raises(ValueError):
                StartNodeArg(record_id + aux_config)

    @pytest.mark.parametrize(
        "arg,expected",
        (
            ["32", {"recordId": 32, "getAdvisors": True, "getDescendants": False}],
            ["32:a", {"recordId": 32, "getAdvisors": True, "getDescendants": False}],
            ["32:d", {"recordId": 32, "getAdvisors": False, "getDescendants": True}],
            ["32:ad", {"recordId": 32, "getAdvisors": True, "getDescendants": True}],
            ["32:da", {"recordId": 32, "getAdvisors": True, "getDescendants": True}],
        ),
    )
    def test_start_node(self, arg: str, expected: StartNodeRequest) -> None:
        sna = StartNodeArg(arg)
        assert sna.start_node == expected


@pytest.mark.parametrize("start_nodes", ([], ["32"], ["32:a"], ["32:d", "14"]))
def test_make_payload(start_nodes: List[str]) -> None:
    start_node_args = [StartNodeArg(sn) for sn in start_nodes]
    assert make_payload(start_node_args) == {
        "kind": "build-graph",
        "startNodes": [sn.start_node for sn in start_node_args],
    }
