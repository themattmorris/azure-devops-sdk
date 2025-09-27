"""Wiql endpoint."""

from http import HTTPMethod
from typing import Any, ClassVar

from ..core import Endpoint


class Wiql(Endpoint):
    """Wiql endpoint."""

    api_version: ClassVar[str] = "7.1"
    path: ClassVar[str] = "wiql"

    def execute(self, *, query: str) -> Any:
        """Execute a query."""
        return self._call(HTTPMethod.POST, payload={"query": query})
