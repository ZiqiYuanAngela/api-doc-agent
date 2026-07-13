from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException

from app.services.openai_parser import OpenApiParseError, parse_openapi_document

router = APIRouter(prefix="/api/specifications", tags = ["Specifications"])
 
SPEC_STORE: dict[str, dict] = {}

@router.post("")
async def upload_specification(file: Annotated[UploadFile, File(...)]) -> dict:
        if not file.filename:
            raise HTTPException(status_code= 400, detail = "A filename is required.")

        content = await file.read()
        if len(content) > 5 * 1024 * 1024:  # 5 MB limit
            raise HTTPException(status_code= 413, detail = "The file size exceeds the 5 MB limit.")
        try:
            document = parse_openapi_document(content, file.filename)
        except OpenApiParseError as exc:
            raise HTTPException(status_code= 400, detail=str(exc))

        spec_id = str(uuid4())
        SPEC_STORE[spec_id] = document

        info = document.get("info", {})
        return {
        "id": spec_id,
        "title": info.get("title", file.filename),
        "version": info.get("version"),
        "openapi_version": document.get(
            "openapi",
            document.get("swagger"),
        ),
        "endpoint_count": count_operations(document),
        }
def count_operations(document: dict) -> int:
    methods = {
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "head",
        "options",
        "trace",
    }

    return sum(
        1
        for path_item in document.get("paths", {}).values()
        if isinstance(path_item, dict)
        for key in path_item
        if key.lower() in methods
    )