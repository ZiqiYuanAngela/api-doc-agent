from typing import Any

from agents import function_tool

from app.services.endpoint_service import (
    get_endpoint_details_impl,
    list_endpoints_impl,
    search_endpoints_impl,
)
from app.services.example_generator import (
    generate_request_example_impl,
)
from app.services.request_validator import (
    validate_request_impl,
)


@function_tool(strict_mode=False)
def list_endpoints(
    specification_id: str,
) -> list[dict[str, Any]]:
    """List operations in an uploaded OpenAPI specification."""
    return list_endpoints_impl(specification_id)


@function_tool(strict_mode=False)
def search_endpoints(
    specification_id: str,
    query: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Find API operations relevant to a natural-language query."""
    return search_endpoints_impl(
        specification_id=specification_id,
        query=query,
        limit=limit,
    )


@function_tool(strict_mode=False)
def get_endpoint_details(
    specification_id: str,
    method: str,
    path: str,
) -> dict[str, Any]:
    """Retrieve parameters, schemas, and responses for an endpoint."""
    return get_endpoint_details_impl(
        specification_id=specification_id,
        method=method,
        path=path,
    )


@function_tool(strict_mode=False)
def generate_request_example(
    specification_id: str,
    method: str,
    path: str,
) -> Any:
    """Generate a deterministic JSON request example."""
    return generate_request_example_impl(
        specification_id=specification_id,
        method=method,
        path=path,
    )


@function_tool(strict_mode=False)
def validate_request(
    specification_id: str,
    method: str,
    path: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    """Validate a JSON payload against an endpoint request schema."""
    return validate_request_impl(
        specification_id=specification_id,
        method=method,
        path=path,
        payload=payload,
    )