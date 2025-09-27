"""Core endpoint/api utilities."""

from __future__ import annotations

import datetime
import os
from http import HTTPMethod
from typing import TYPE_CHECKING, Any, ClassVar, TypedDict, Unpack, get_type_hints

import requests
from dotenv import load_dotenv


load_dotenv()


if TYPE_CHECKING:
    from . import Client


class ListResponse(TypedDict):
    """Response when listing all entities."""

    count: int
    value: list[dict[str, Any]]


class Resource(TypedDict):
    """Resource info."""

    id: int
    type: str


class ClientConfiguration(TypedDict, total=False):
    """Client configuration items."""

    organization: str
    project: str


class _BaseClient:
    def __init__(self, **kwargs: Unpack[ClientConfiguration]) -> None:
        self.organization = (
            kwargs.get("organization") or os.environ["AZURE_DEVOPS_ORGANIZATION"]
        )
        self.project = kwargs.get("project") or os.environ["AZURE_DEVOPS_PROJECT"]


class Api(_BaseClient):
    """An Azure DevOps API."""

    api_version: ClassVar[str] = "7.2-preview.3"
    path: ClassVar[str | None] = None

    def __init__(self, *parts: str, **kwargs: Unpack[ClientConfiguration]) -> None:  # noqa: D107
        super().__init__(**kwargs)
        self.parts = [*parts, self.path or type(self).__name__.lower()]

    @property
    def url(self) -> str:
        """Endpoint URL."""
        return "/".join(
            [
                "https://dev.azure.com/",
                self.organization,
                self.project,
                "_apis",
                *self.parts,
            ]
        )


class Endpoint(Api):
    """An Azure DevOps endpoint."""

    def _call(
        self,
        method: HTTPMethod,
        *url_parts: Any,
        params: dict[str, Any] | None = None,
        payload: Any | None = None,
        headers: dict[str, Any] | None = None,
        data: requests.sessions._Data | None = None,
    ) -> Any:
        response = requests.request(
            str(method),
            (sep := "/").join(
                [
                    self.url.strip(sep),
                    *[str(url_part).strip(sep) for url_part in url_parts],
                ]
            ),
            params={
                k: v.isoformat() if isinstance(v, datetime.datetime) else v
                for k, v in ((params or {}) | {"api-version": self.api_version}).items()
            },
            auth=("", os.environ["AZURE_DEVOPS_PAT"]),
            headers={"Accept": "application/json"} | (headers or {}),
            json=payload,
            data=data,
            timeout=60,
        )
        return response.json()

    def list_all(self, **params: Any) -> list[dict[str, Any]]:
        """List all entities in endpoint."""
        list_response: ListResponse = self._call(HTTPMethod.GET, params=params)
        return list_response["value"]

    def get(self, id: int, /) -> dict[str, Any]:
        """Get an entity by id."""
        return self._call(HTTPMethod.GET, id)


class endpoint(property):  # noqa: N801
    """Property that returns an instance of the annotated type."""

    def __get__(
        self,
        instance: Client | Api | None,
        owner: type[Client | Api],
    ) -> Api:
        """Return the app/endpoint type."""
        if instance:
            return_type: type[Api] = get_type_hints(self.fget)["return"]
            parts = instance.parts if isinstance(instance, Api) else []
            return return_type(
                *parts,
                organization=instance.organization,
                project=instance.project,
            )

        return super().__get__(instance, owner)  # type: ignore[return-value]


api = endpoint
