"""Work items endpoint."""

from http import HTTPMethod
from typing import Any, ClassVar, Literal, TypeAlias, TypedDict, Unpack

from ..core import Endpoint


RelationshipName: TypeAlias = Literal[  # noqa: UP040
    "Affected By",
    "Affects",
    "Artifact Link",
    "Attached File",
    "Child",
    "Duplicate Of",
    "Duplicate",
    "Hyperlink",
    "Parent",
    "Predecessor",
    "Referenced By",
    "References",
    "Related",
    "Shared Steps",
    "Successor",
    "Test Case",
    "Tested By",
    "Tests",
]

RELATIONSHIP_MAPPING: dict[RelationshipName, str] = {
    "Affected By": "Microsoft.VSTS.Common.Affects-Reverse",
    "Affects": "Microsoft.VSTS.Common.Affects-Forward",
    "Artifact Link": "ArtifactLink",
    "Attached File": "AttachedFile",
    "Child": "System.LinkTypes.Hierarchy-Forward",
    "Duplicate": "System.LinkTypes.Duplicate-Forward",
    "Duplicate Of": "System.LinkTypes.Duplicate-Reverse",
    "Hyperlink": "Hyperlink",
    "Parent": "System.LinkTypes.Hierarchy-Reverse",
    "Predecessor": "System.LinkTypes.Dependency-Reverse",
    "Referenced By": "Microsoft.VSTS.TestCase.SharedParameterReferencedBy-Forward",
    "References": "Microsoft.VSTS.TestCase.SharedParameterReferencedBy-Reverse",
    "Related": "System.LinkTypes.Related",
    "Shared Steps": "Microsoft.VSTS.TestCase.SharedStepReferencedBy-Reverse",
    "Successor": "System.LinkTypes.Dependency-Forward",
    "Test Case": "Microsoft.VSTS.TestCase.SharedStepReferencedBy-Forward",
    "Tested By": "Microsoft.VSTS.Common.TestedBy-Forward",
    "Tests": "Microsoft.VSTS.Common.TestedBy-Reverse",
}
"""https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/work-item-relation-types/list"""

ItemType: TypeAlias = Literal["Task", "Bug", "Feature", "User Story"]  # noqa: UP040


class Relationship(TypedDict):
    """How one work item relates to another work item."""

    work_item_id: int
    relationship_type: RelationshipName


class PatchOperation(TypedDict):
    """Patch operation."""

    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    path: str
    value: Any


class WorkItemParams(TypedDict, total=False):
    """Parameters for creating, updating work item."""

    title: str
    tags: list[str]
    state: Literal["New", "Active", "Closed", "Removed"]
    description: str
    area: str
    relations: list[Relationship]
    iteration: str
    assigned_to: str
    validate_only: bool
    bypass_rules: bool
    suppress_notifications: bool
    acceptance_criteria: list[str]


class WorkItemResponse(TypedDict):
    """Response returned when creating work item."""

    id: int
    rev: int
    fields: dict[str, Any]
    url: str


class WorkItems(Endpoint):
    """Work items endpoint."""

    path: ClassVar[str] = "workitems"

    def _create_or_update(
        self,
        method: HTTPMethod,
        *url_parts: Any,
        **kwargs: Unpack[WorkItemParams],
    ) -> WorkItemResponse:
        ops: list[PatchOperation] = []

        if (tags := kwargs.get("tags")) is not None:
            ops.append(
                PatchOperation(
                    op="add",
                    path="/fields/System.Tags",
                    value=";".join(tags),
                )
            )

        if relations := kwargs.get("relations"):
            ops.extend(
                [
                    PatchOperation(
                        op="add",
                        path="/relations/-",
                        value={
                            "rel": RELATIONSHIP_MAPPING[relation["relationship_type"]],
                            "url": "/".join([self.url, str(relation["work_item_id"])]),
                        },
                    )
                    for relation in relations
                ]
            )

        if acceptance_criteria := kwargs.get("acceptance_criteria"):
            field_name = "Microsoft.VSTS.Common.AcceptanceCriteria"
            ops.extend(
                [
                    PatchOperation(
                        op="add",
                        path=f"/multilineFieldsFormat/{field_name}",
                        value="Markdown",
                    ),
                    PatchOperation(
                        op="add",
                        path=f"/fields/{field_name}",
                        value="\n".join(
                            f"* {criterion}" for criterion in acceptance_criteria
                        ),
                    ),
                ]
            )

        for k, v in {
            "State": kwargs.get("state"),
            "AssignedTo": kwargs.get("assigned_to"),
            "IterationPath": kwargs.get("iteration"),
            "Title": kwargs.get("title"),
            "Description": kwargs.get("description"),
            "AreaPath": kwargs.get("area"),
        }.items():
            if v:
                op = PatchOperation(op="add", path=f"/fields/System.{k}", value=v)
                ops.append(op)

        return self._call(
            method,
            *url_parts,
            headers={"Content-Type": "application/json-patch+json"},
            payload=ops or None,
            params={
                "validateOnly": kwargs.get("validate_only", False),
                "bypassRules": kwargs.get("bypass_rules", False),
                "suppressNotifications": kwargs.get("suppress_notifications", False),
            },
        )

    def create(
        self,
        item_type: ItemType,
        **kwargs: Unpack[WorkItemParams],
    ) -> WorkItemResponse:
        """Create a work item."""
        return self._create_or_update(HTTPMethod.POST, f"${item_type}", **kwargs)

    def update(
        self,
        work_item_id: int,
        **kwargs: Unpack[WorkItemParams],
    ) -> WorkItemResponse:
        """Update a work item."""
        return self._create_or_update(HTTPMethod.PATCH, work_item_id, **kwargs)
