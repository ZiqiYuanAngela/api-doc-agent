from typing import Any


def generate_example_from_schema(
    schema: dict[str, Any],
) -> Any:
    if "example" in schema:
        return schema["example"]

    if "default" in schema:
        return schema["default"]

    enum_values = schema.get("enum")
    if enum_values:
        return enum_values[0]

    schema_type = schema.get("type")

    if schema_type == "object" or "properties" in schema:
        required_fields = set(schema.get("required", []))
        result: dict[str, Any] = {}

        for name, property_schema in schema.get(
            "properties",
            {},
        ).items():
            if name in required_fields or len(result) < 3:
                result[name] = generate_example_from_schema(
                    property_schema
                )

        return result

    if schema_type == "array":
        return [
            generate_example_from_schema(
                schema.get("items", {})
            )
        ]

    if schema_type == "integer":
        return 1

    if schema_type == "number":
        return 1.0

    if schema_type == "boolean":
        return True

    if schema_type == "string":
        examples_by_format = {
            "email": "customer@example.com",
            "date": "2026-07-12",
            "date-time": "2026-07-12T12:00:00Z",
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
        }

        return examples_by_format.get(
            schema.get("format"),
            "string",
        )

    return None

from typing import Any

from app.services.endpoint_service import get_endpoint_details_impl


def generate_request_example_impl(
    specification_id: str,
    method: str,
    path: str,
) -> Any:
    endpoint = get_endpoint_details_impl(
        specification_id=specification_id,
        method=method,
        path=path,
    )

    request_body = endpoint.get("request_body", {})
    content = request_body.get("content", {})
    media_type = content.get("application/json", {})
    schema = media_type.get("schema")

    if not schema:
        raise ValueError(
            f"No application/json request schema found for "
            f"{method.upper()} {path}"
        )

    return generate_example_from_schema(schema)