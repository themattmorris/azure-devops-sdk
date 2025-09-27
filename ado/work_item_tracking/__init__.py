"""Work item tracking (wit) API."""

from ..core import Api, endpoint
from .wiql import Wiql
from .work_items import WorkItems


class Wit(Api):
    """[Work item tracking API](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/?view=azure-devops-rest-7.2)."""

    @endpoint
    def work_items(self) -> WorkItems:
        """Work items endpoint."""

    @endpoint
    def wiql(self) -> Wiql:
        """Wiql endpoint."""
