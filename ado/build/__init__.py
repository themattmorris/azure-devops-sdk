"""Build API."""

from ..core import Api, endpoint
from .definitions import Definitions


class Build(Api):
    """[Build API](https://learn.microsoft.com/en-us/rest/api/azure/devops/build/?view=azure-devops-rest-7.2)."""

    @endpoint
    def definitions(self) -> Definitions:
        """Definitions endpoint."""
