from geneagrapher.geneagrapher import (
    Geneagraph,
    GgrapherError,
    RecordId,
    RequestPayload,
    StartNodeArg,
    StartNodeRequest,
    get_graph,
    make_payload,
)

import json
import pytest
from typing import Dict, List
from unittest.mock import AsyncMock, patch, sentinel as s
from websockets.exceptions import WebSocketException


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


class TestGgrapherError:
    @pytest.mark.parametrize(
        "msg,extra,expected_str",
        (
            [
                "The message",
                {"Foo": "Blah", "Baz": "Bleh"},
                """The message

If this problem persists, please create an issue at
https://github.com/davidalber/geneagrapher/issues/new, and include the
following in the issue body:

    Message: The message
    Command: {command}
    Foo:     Blah
    Baz:     Bleh""",
            ],
            [
                "The message",
                {},
                """The message

If this problem persists, please create an issue at
https://github.com/davidalber/geneagrapher/issues/new, and include the
following in the issue body:

    Message: The message
    Command: {command}""",
            ],
        ),
    )
    def test_str(self, msg: str, extra: Dict[str, str], expected_str: str) -> None:
        command = ["a", "b", "c"]
        with patch("geneagrapher.geneagrapher.sys.argv", command):
            e = GgrapherError(msg, extra=extra)
            assert str(e) == expected_str.format(command=" ".join(command))


@pytest.mark.parametrize("start_nodes", ([], ["32"], ["32:a"], ["32:d", "14"]))
def test_make_payload(start_nodes: List[str]) -> None:
    start_node_args = [StartNodeArg(sn) for sn in start_nodes]
    assert make_payload(start_node_args) == {
        "kind": "build-graph",
        "options": {"reportingCallback": True},
        "startNodes": [sn.start_node for sn in start_node_args],
    }


class TestGetGraph:
    @pytest.mark.asyncio
    @patch("geneagrapher.geneagrapher.websockets.client.connect")
    async def test_good(self, m_ws_connect: AsyncMock) -> None:
        request_payload: RequestPayload = {
            "kind": "build-graph",
            "options": {"reportingCallback": True},
            "startNodes": [
                {"recordId": 6, "getAdvisors": True, "getDescendants": False}
            ],
        }
        graph: Geneagraph = {
            "start_nodes": [RecordId(6)],
            "nodes": {
                RecordId(6): {
                    "id": RecordId(6),
                    "name": "Name",
                    "institution": None,
                    "year": None,
                    "descendants": [],
                    "advisors": [],
                }
            },
            "status": "complete",
        }
        response_payload = {"kind": "graph", "payload": graph}

        ws_conn = AsyncMock()
        ws_conn.recv.return_value = json.dumps(response_payload)
        m_ws_connect.return_value.__aenter__.return_value = ws_conn

        with patch("geneagrapher.geneagrapher.GGRAPHER_URI", s.uri):
            assert await get_graph(request_payload) == response_payload["payload"]

        m_ws_connect.assert_called_once_with(s.uri)
        ws_conn.send.assert_called_once_with(json.dumps(request_payload))
        ws_conn.recv.assert_called_once_with()

    @pytest.mark.asyncio
    @patch("geneagrapher.geneagrapher.websockets.client.connect")
    async def test_bad_request(self, m_ws_connect: AsyncMock) -> None:
        request_payload: RequestPayload = {
            "kind": "build-graph",
            "options": {"reportingCallback": True},
            "startNodes": [
                {"recordId": 6, "getAdvisors": True, "getDescendants": False}
            ],
        }
        response_payload_json = json.dumps({"kind": "something"})

        ws_conn = AsyncMock()
        ws_conn.recv.return_value = response_payload_json
        m_ws_connect.return_value.__aenter__.return_value = ws_conn

        with patch("geneagrapher.geneagrapher.GGRAPHER_URI", s.uri):
            with pytest.raises(GgrapherError) as exc_info:
                await get_graph(request_payload)

        assert exc_info.value.msg == "Request to Geneagrapher backend failed."
        assert exc_info.value.extra == {"Response": response_payload_json}

        m_ws_connect.assert_called_once_with(s.uri)
        ws_conn.send.assert_called_once_with(json.dumps(request_payload))
        ws_conn.recv.assert_called_once_with()

    @pytest.mark.asyncio
    @patch("geneagrapher.geneagrapher.websockets.client.connect")
    async def test_bad_socket(self, m_ws_connect: AsyncMock) -> None:
        request_payload: RequestPayload = {
            "kind": "build-graph",
            "options": {"reportingCallback": True},
            "startNodes": [
                {"recordId": 6, "getAdvisors": True, "getDescendants": False}
            ],
        }

        m_ws_connect.return_value.__aenter__.side_effect = WebSocketException()

        with patch("geneagrapher.geneagrapher.GGRAPHER_URI", s.uri):
            with pytest.raises(GgrapherError) as exc_info:
                await get_graph(request_payload)

        assert exc_info.value.msg == "Geneagrapher backend is currently unavailable."

        m_ws_connect.assert_called_once_with(s.uri)
