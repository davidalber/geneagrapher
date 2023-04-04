"""This module implements `IdentityOutput`, a class that outputs a
Geneagraph JSON structure. This is simply the structure that is
returned by the Geneagrapher backend.
"""

from ..types import Geneagraph

import json


class IdentityOutput:
    def __init__(self, graph: Geneagraph) -> None:
        self.graph = graph

    @property
    def output(self) -> str:
        return json.dumps(self.graph)
