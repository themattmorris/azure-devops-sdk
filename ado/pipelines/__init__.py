"""Pipelines API."""

from ..core import Api, endpoint
from .pipeline_permissions import PipelinePermissions


class Pipelines(Api):
    """[Pipelines API](https://learn.microsoft.com/en-us/rest/api/azure/devops/pipelines/?view=azure-devops-rest-7.2)."""

    @endpoint
    def pipeline_permissions(self) -> PipelinePermissions:
        """Pipeline permissions endpoint."""
