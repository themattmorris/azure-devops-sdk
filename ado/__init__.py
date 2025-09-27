"""Azure DevOps python SDK."""

__version__ = "v0"

from .build import Build
from .core import _BaseClient, api
from .distributed_task import DistributedTask
from .git import Git
from .pipelines import Pipelines
from .work_item_tracking import Wit


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

    @api
    def wit(self) -> Wit:
        """Work item tracking API."""
