from typing import Any

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options", "trace"}

def build_endpoint_index(specification: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Build an index of API endpoints from the OpenAPI document.

    Args:
        document (dict): The OpenAPI document."""
    endpoints: list[dict[str, Any]] = []

    for path, path_item in specification.get("paths", {}).items():
        if not isinstance(path_item, dict):
            continue

        shared_parameters = path_item.get("parameters", [])

        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS:
                continue

            if not isinstance(operation, dict):
                continue

            parameters = [
                *shared_parameters,
                *operation.get("parameters", []),
            ]

            endpoint = {
                "method": method.upper(),
                "path": path,
                "operation_id": operation.get("operationId"),
                "summary": operation.get("summary"),
                "description": operation.get("description"),
                "tags": operation.get("tags", []),
                "parameters": parameters,
                "request_body": operation.get("requestBody"),
                "responses": operation.get("responses", {}),
            }

            endpoints.append(endpoint)

    return endpoints

    # endpoints = build_endpoint_index(specification)

    # assert len(endpoints) == 1
    # assert endpoints[0]["method"] == "POST"
    # assert endpoints[0]["path"] == "/customers"
    # print("Test passed: build_endpoint_index works as expected.")
