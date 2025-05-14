"""Repositories endpoint."""

from typing import TYPE_CHECKING, TypedDict, Unpack

from ..core import Endpoint
from ..models import ProjectInfo


class RepositoriesParameters(TypedDict, total=False):
    """Parameters that are inputs for getting repos."""

    includeAllUrls: bool
    """True to include all remote URLs. The default value is false."""

    includeHidden: bool
    """True to include hidden repositories. The default value is false."""

    includeLinks: bool
    """True to include reference links. The default value is false."""


class RepoInfo(TypedDict):
    """Repo info."""

    defaultBranch: str
    id: str
    isDisabled: bool
    isInMaintenance: bool
    name: str
    project: ProjectInfo
    remoteUrl: str
    size: int
    sshUrl: str
    url: str
    webUrl: str


class Repositories(Endpoint):
    """[Repositories endpoint](https://learn.microsoft.com/en-us/rest/api/azure/devops/git/repositories?view=azure-devops-rest-7.2)."""

    if TYPE_CHECKING:

        def list_all(self, **params: Unpack[RepositoriesParameters]) -> list[RepoInfo]:
            """List all repositories."""
