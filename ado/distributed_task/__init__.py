"""Distributed task API."""

from ..core import Api, endpoint
from .variable_groups import VariableGroups


class DistributedTask(Api):
    """[Distributed task endpoint](https://learn.microsoft.com/en-us/rest/api/azure/devops/distributedtask/?view=azure-devops-rest-7.2)."""

    @endpoint
    def variable_groups(self) -> VariableGroups:
        """Variable groups endpoint."""
