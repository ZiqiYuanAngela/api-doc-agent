import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.openai_parser import OpenApiParseError, parse_openapi_document


def test_parse_openapi_document_supports_json_bytes():
    payload = b'{"openapi": "3.0.0", "info": {"title": "Test", "version": "1.0"}}'

    document = parse_openapi_document(payload, "spec.json")

    assert document["openapi"] == "3.0.0"
    assert document["info"]["title"] == "Test"


def test_parse_openapi_document_rejects_empty_content():
    with pytest.raises(OpenApiParseError, match="empty"):
        parse_openapi_document(b"", "spec.yaml")


def test_parse_openapi_document_rejects_non_object_root():
    with pytest.raises(OpenApiParseError, match="object at its root"):
        parse_openapi_document(b"[]", "spec.json")
