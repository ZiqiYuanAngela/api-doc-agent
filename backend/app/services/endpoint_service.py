from typing import Any

from app.repositories.specification_repository import (
    specification_repository,
)
from app.services.endpoint_index import build_endpoint_index
from app.services.endpoint_search import search_endpoint_index
from app.services.reference_resolver import resolve_schema


def list_endpoints_impl(
    specification_id: str,
) -> list[dict[str, Any]]:
    specification = specification_repository.get(specification_id)
    endpoints = build_endpoint_index(specification)

    return [
        {
            "method": endpoint["method"],
            "path": endpoint["path"],
            "operation_id": endpoint["operation_id"],
            "summary": endpoint["summary"],
            "tags": endpoint["tags"],
        }
        for endpoint in endpoints
    ]


def search_endpoints_impl(
    specification_id: str,
    query: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    specification = specification_repository.get(specification_id)

    return search_endpoint_index(
        specification=specification,
        query=query,
        limit=limit,
    )


def get_endpoint_details_impl(
    specification_id: str,
    method: str,
    path: str,
) -> dict[str, Any]:
    specification = specification_repository.get(specification_id)
    endpoints = build_endpoint_index(specification)

    for endpoint in endpoints:
        if (
            endpoint["method"].upper() == method.upper()
            and endpoint["path"] == path
        ):
            return resolve_schema(
                root=specification,
                value=endpoint,
            )

    raise ValueError(
        f"Endpoint not found: {method.upper()} {path}"
    )