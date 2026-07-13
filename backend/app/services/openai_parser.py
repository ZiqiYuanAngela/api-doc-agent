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
    if not isinstance(document, dict):
        raise OpenApiParseError(
            "The OpenAPI document must contain an object at its root."
        )

    if "openapi" not in document and "swagger" not in document:
        raise OpenApiParseError(
            "The file does not appear to be an OpenAPI specification."
        )

    info = document.get("info")
    if not isinstance(info, dict):
        raise OpenApiParseError(
            "The OpenAPI document must include an info object."
        )

    if not info.get("title") or not info.get("version"):
        raise OpenApiParseError(
            "The OpenAPI document must include info.title and info.version."
        )


def parse_openapi_document(content: bytes, filename: str) -> dict[str, Any]:
    if not isinstance(content, (bytes, bytearray)):
        raise OpenApiParseError("The uploaded file must be provided as bytes.")

    if not content.strip():
        raise OpenApiParseError("The uploaded file is empty.")

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
            if yaml is None:
                raise OpenApiParseError("YAML support is not available.")
            document = yaml.safe_load(text)
        else:
            raise OpenApiParseError(
                "Only JSON, YAML, and YML files are supported."
            )
    except json.JSONDecodeError as exc:
        raise OpenApiParseError("The uploaded file is not valid JSON.") from exc
    except Exception as exc:
        if isinstance(exc, OpenApiParseError):
            raise
        raise OpenApiParseError("The uploaded file is not valid YAML.") from exc

    validate_openapi_header(document)
    return document

    
