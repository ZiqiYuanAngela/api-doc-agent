import re
from typing import Any

from app.services.endpoint_index import build_endpoint_index


def tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) > 1
    }


def search_endpoint_index(
    specification: dict[str, Any],
    query: str,
    limit: int = 5,
) -> list[dict[str, Any]]:
    endpoints = build_endpoint_index(specification)
    query_tokens = tokenize(query)

    ranked: list[tuple[int, dict[str, Any]]] = []

    for endpoint in endpoints:
        searchable_text = " ".join(
            [
                endpoint.get("method", ""),
                endpoint.get("path", ""),
                endpoint.get("operation_id") or "",
                endpoint.get("summary") or "",
                endpoint.get("description") or "",
                " ".join(endpoint.get("tags", [])),
            ]
        )

        endpoint_tokens = tokenize(searchable_text)
        score = len(query_tokens & endpoint_tokens)

        if score > 0:
            ranked.append((score, endpoint))

    ranked.sort(key=lambda item: item[0], reverse=True)

    return [
        {
            "method": endpoint["method"],
            "path": endpoint["path"],
            "operation_id": endpoint["operation_id"],
            "summary": endpoint["summary"],
            "score": score,
        }
        for score, endpoint in ranked[:limit]
    ]