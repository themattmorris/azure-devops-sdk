"""Core models that are used throughout."""

from typing import Literal, TypedDict


class UserInfo(TypedDict):
    """User info."""

    displayName: str
    id: str
    uniqueName: str


class AuthorizedByInfo(UserInfo):
    """Authorized by info."""

    descriptor: str


class AuthoredByInfo(AuthorizedByInfo):
    """Authored by user info."""

    imageUrl: str
    url: str


class PoolInfo(TypedDict):
    """Pool info."""

    id: int
    isHosted: bool
    name: str


class QueueInfo(TypedDict):
    """Queue info."""

    id: int
    name: str
    pool: PoolInfo
    url: str


class ProjectInfo(TypedDict):
    """Project info."""

    description: str
    id: str
    lastUpdateTime: str
    name: str
    revision: int
    state: Literal[
        "all",
        "createPending",
        "deleted",
        "deleting",
        "new",
        "unchanged",
        "wellFormed",
    ]
    url: str
    visibility: Literal["public", "private"]
