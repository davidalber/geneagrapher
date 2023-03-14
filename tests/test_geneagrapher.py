from geneagrapher.geneagrapher import RecordIdArg

import pytest


class TestRecordIdArg:
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
    def test_init(self, record_id, record_id_valid, aux_config, aux_config_valid):
        if record_id_valid and aux_config_valid:
            rid = RecordIdArg(record_id + aux_config)
            assert rid.record_id == int(record_id)
            assert rid.request_advisors is ("a" in aux_config)
            assert rid.request_descendants is ("d" in aux_config)
        else:
            with pytest.raises(ValueError):
                RecordIdArg(record_id + aux_config)
