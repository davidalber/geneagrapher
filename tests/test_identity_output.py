from geneagrapher.output.identity import IdentityOutput

from unittest.mock import MagicMock, patch, sentinel as s


class TestIdentityOutput:
    def test_init(self) -> None:
        do = IdentityOutput(s.graph)
        assert do.graph == s.graph

    @patch("geneagrapher.output.identity.json")
    def test_output(self, m_json: MagicMock) -> None:
        m_json.dumps = MagicMock(return_value=s.the_json)

        do = IdentityOutput(s.graph)
        assert do.output == s.the_json

        m_json.dumps.assert_called_once_with(s.graph)
