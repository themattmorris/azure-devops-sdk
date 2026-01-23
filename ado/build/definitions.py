"""Definitions endpoint."""

import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Literal, TypedDict, Unpack

from ..core import Endpoint
from ..models import AuthoredByInfo, ProjectInfo, QueueInfo


class DefinitionInfo(TypedDict):
    """Build definition info."""

    authoredBy: AuthoredByInfo
    createdDate: str
    drafts: list[Any]
    id: int
    name: str
    path: str | None
    project: ProjectInfo
    quality: str
    queue: QueueInfo
    revision: int
    type: str
    uri: str
    url: str


class DefinitionsParameters(TypedDict, total=False):
    """Parameters that are inputs for getting build definitions."""

    builtAfter: datetime.datetime
    """If specified, filters to definitions that have builds after this date."""

    continuationToken: str
    """A continuation token, returned by a previous call to this method, that can be
    used to return the next set of definitions.
    """

    definitionIds: list[int]
    """A list that specifies the IDs of definitions to retrieve."""

    includeAllProperties: bool
    """Indicates whether the full definitions should be returned. By default, shallow
    representations of the definitions are returned.
    """

    includeLatestBuilds: bool
    """Indicates whether to return the latest and latest completed builds for this
    definition.
    """

    minMetricsTime: datetime.datetime
    """If specified, indicates the date from which metrics should be included."""

    name: str
    """If specified, filters to definitions whose names match this pattern."""

    notBuiltAfter: datetime.datetime
    """If specified, filters to definitions that do not have builds after this date."""

    path: str
    """If specified, filters to definitions under this folder."""

    processType: int
    """If specified, filters to definitions with the given process type."""

    queryOrder: Literal[
        "definitionNameAscending",
        "definitionNameDescending",
        "lastModifiedAscending",
        "lastModifiedDescending",
        "none",
    ]
    """Indicates the order in which definitions should be returned."""

    repositoryId: str
    """A repository ID. If specified, filters to definitions that use this repository.
    """

    repositoryType: str
    """If specified, filters to definitions that have a repository of this type."""

    taskIdFilter: str
    """If specified, filters to definitions that use the specified task."""

    yamlFilename: str
    """If specified, filters to YAML definitions that match the given filename. To use
    this filter includeAllProperties should be set to true.
    """


class Definitions(Endpoint):
    """[Definitions endpoint](https://learn.microsoft.com/en-us/rest/api/azure/devops/build/definitions/list?view=azure-devops-rest-7.2)."""

    api_version: ClassVar[str] = "7.2-preview.7"

    if TYPE_CHECKING:

        def list_all(
            self,
            **params: Unpack[DefinitionsParameters],
        ) -> list[DefinitionInfo]:
            """List all repositories."""
