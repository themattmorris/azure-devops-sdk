"""Variable groups endpoint."""

from typing import TYPE_CHECKING, Any, TypedDict

from ..core import Endpoint
from ..models import UserInfo


class VariableInfo(TypedDict):
    """Variable info."""

    value: str


class VariableGroupInfo(TypedDict):
    """Variable group info."""

    createdBy: UserInfo
    createdOn: str
    description: str
    id: int
    isShared: bool
    modifiedBy: UserInfo
    name: str
    type: str
    variableGroupProjectReferences: Any
    variables: dict[str, VariableInfo]


class VariableGroups(Endpoint):
    """Variable groups endpoint."""

    if TYPE_CHECKING:

        def list_all(self) -> list[VariableGroupInfo]:
            """List all variable groups."""
