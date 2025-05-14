"""Azure DevOps python SDK."""

__version__ = "v0"

from .build import Build
from .core import _BaseClient, api
from .distributed_task import DistributedTask
from .git import Git
from .pipelines import Pipelines


class Client(_BaseClient):
    """Azure DevOps client."""

    @api
    def distributed_task(self) -> DistributedTask:
        """Distributed task API."""

    @api
    def pipelines(self) -> Pipelines:
        """Pipelines API."""

    @api
    def git(self) -> Git:
        """Repositories API."""

    @api
    def build(self) -> Build:
        """Build API."""
