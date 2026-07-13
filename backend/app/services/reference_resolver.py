# app/services/reference_resolver.py

from copy import deepcopy
from typing import Any


class ReferenceResolutionError(ValueError):
    pass


def resolve_local_reference(
    root: dict[str, Any],
    reference: str,
) -> Any:
    if not reference.startswith("#/"):
        raise ReferenceResolutionError(
            f"Only local references are supported: {reference}"
        )

    current: Any = root

    for segment in reference[2:].split("/"):
        segment = segment.replace("~1", "/").replace("~0", "~")

        if not isinstance(current, dict) or segment not in current:
            raise ReferenceResolutionError(
                f"Reference could not be resolved: {reference}"
            )

        current = current[segment]

    return deepcopy(current)

def resolve_schema(
    root: dict[str, Any],
    value: Any,
    depth: int = 0,
    max_depth: int = 20,
) -> Any:
    if depth > max_depth:
        raise ReferenceResolutionError(
            "Maximum reference depth exceeded."
        )

    if isinstance(value, list):
        return [
            resolve_schema(root, item, depth + 1, max_depth)
            for item in value
        ]

    if not isinstance(value, dict):
        return value

    if "$ref" in value:
        resolved = resolve_local_reference(root, value["$ref"])

        sibling_fields = {
            key: item
            for key, item in value.items()
            if key != "$ref"
        }

        if isinstance(resolved, dict):
            resolved.update(sibling_fields)

        return resolve_schema(
            root,
            resolved,
            depth + 1,
            max_depth,
        )

    return {
        key: resolve_schema(root, item, depth + 1, max_depth)
        for key, item in value.items()
    }