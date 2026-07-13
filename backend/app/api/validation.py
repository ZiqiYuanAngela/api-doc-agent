from fastapi import APIRouter, HTTPException

from app.models.response import ValidateRequestBody
from app.repositories.specification_repository import (
    SpecificationNotFoundError,
)
from app.services.request_validator import validate_request_impl


router = APIRouter(
    prefix="/api/validation",
    tags=["validation"],
)


@router.post("/request")
async def validate_request_body(
    request: ValidateRequestBody,
) -> dict:
    try:
        return validate_request_impl(
            specification_id=request.specification_id,
            method=request.method,
            path=request.path,
            payload=request.payload,
        )

    except SpecificationNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc