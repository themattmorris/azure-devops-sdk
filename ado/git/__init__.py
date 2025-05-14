"""Git API."""

from ..core import Api, endpoint
from .repositories import Repositories


class Git(Api):
    """[Git API](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/?view=azure-devops-rest-7.2)."""

    @endpoint
    def repositories(self) -> Repositories:
        """Repositories endpoint."""
