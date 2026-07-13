"""Utilities for parsing uploaded OpenAPI specifications."""
from __future__ import annotations

import json
from typing import Any

try:
    import yaml  # PyYAML
except Exception:  # pragma: no cover - runtime import
    yaml = None

__all__ = ["OpenApiParseError", "parse_openapi_document"]


class OpenApiParseError(ValueError):
    """Raised when an uploaded OpenAPI document cannot be parsed or validated."""


def validate_openapi_header(document: dict[str, Any]) -> None:
    if "openapi" not in document and "swagger" not in document:
        raise OpenApiParseError(
            "The file does not appear to be an OpenAPI specification."
        )

    if "paths" not in document:
        raise OpenApiParseError(
            "The OpenAPI specification does not contain a paths section."
        )


def parse_openapi_document(content: bytes, filename: str) -> dict[str, Any]:
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise OpenApiParseError(
            "The specification must be UTF-8 encoded."
        ) from exc

    try:
        if filename.lower().endswith(".json"):
            document = json.loads(text)
        elif filename.lower().endswith((".yaml", ".yml")):
            document = yaml.safe_load(text)
        else:
            raise OpenApiParseError(
                "Only JSON, YAML, and YML files are supported."
            )
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise OpenApiParseError(
            "The uploaded file is not valid JSON or YAML."
        ) from exc

    if not isinstance(document, dict):
        raise OpenApiParseError(
            "The OpenAPI document must contain an object at its root."
        )

    validate_openapi_header(document)
    return document

    
