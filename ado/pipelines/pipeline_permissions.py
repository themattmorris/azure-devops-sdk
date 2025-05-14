"""Pipeline permissions endpoint."""

from http import HTTPMethod
from typing import ClassVar, TypedDict

from ..core import Endpoint, Resource, endpoint
from ..models import AuthorizedByInfo


class VariableGroupPermissionPatch(TypedDict):
    """Variable group permission patch setting."""

    authorized: bool
    id: int


class VariableGroupPermissionInfo(VariableGroupPermissionPatch):
    """Variable group permission info."""

    authorizedBy: AuthorizedByInfo
    authorizedOn: str


class VariableGroupPermissionResponse(TypedDict):
    """Response when getting variable group permissions."""

    pipelines: list[VariableGroupPermissionInfo]
    resource: Resource


class VariableGroupPermissions(Endpoint):
    """Variable group permissions endpoint."""

    path: ClassVar[str] = "variablegroup"
    api_version: ClassVar[str] = "7.1-preview.1"

    def grant(self, /, variable_group_id: int, *, pipeline_ids: list[int]):  # type: ignore[no-untyped-def]
        """Grant pipelines permissions to a variable group."""
        # Get all the current permissions
        payload = {
            "pipelines": [
                *[
                    VariableGroupPermissionPatch(
                        id=pipeline_id,
                        authorized=True,
                    )
                    for pipeline_id in pipeline_ids
                ],
                [
                    VariableGroupPermissionPatch(
                        id=permissions_id,
                        authorized=permissions["authorized"],
                    )
                    for permissions in self.get(variable_group_id)
                    if (permissions_id := permissions["id"]) not in pipeline_ids
                ],
            ]
        }
        return self._call(HTTPMethod.PATCH, variable_group_id, payload=payload)

    def get(self, /, variable_group_id: int) -> list[VariableGroupPermissionInfo]:
        """Get variable group permissions."""
        response: VariableGroupPermissionResponse = super().get(variable_group_id)  # type: ignore[assignment]
        return response["pipelines"]


class PipelinePermissions(Endpoint):
    """Pipeline permissions endpoint."""

    path: ClassVar[str] = "pipelinePermissions"

    @endpoint
    def variable_groups(self) -> VariableGroupPermissions:
        """Variable group permissions endpoint."""
