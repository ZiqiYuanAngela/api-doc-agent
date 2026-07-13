from typing import Any

from jsonschema import Draft202012Validator

from app.services.endpoint_service import get_endpoint_details_impl


def validate_json_instance(
    instance: Any,
    schema: dict[str, Any],
) -> dict[str, Any]:
    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )

    return {
        "valid": not errors,
        "errors": [
            {
                "path": ".".join(
                    str(segment)
                    for segment in error.absolute_path
                ),
                "message": error.message,
                "validator": error.validator,
            }
            for error in errors
        ],
    }


def validate_request_impl(
    specification_id: str,
    method: str,
    path: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
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
        return {
            "valid": False,
            "errors": [
                {
                    "path": "",
                    "message": (
                        "No application/json request schema "
                        "was found for this endpoint."
                    ),
                    "validator": None,
                }
            ],
        }

    return validate_json_instance(
        instance=payload,
        schema=schema,
    )