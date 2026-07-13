from fastapi import APIRouter, HTTPException

from app.agents.documentation_agent import (
    answer_documentation_question,
)
from app.models.response import (
    AskQuestionRequest,
    DocumentationAnswer,
)
from app.api.specifications import SPEC_STORE
from app.repositories.specification_repository import (
    specification_repository,
)

router = APIRouter(
    prefix="/api/questions",
    tags=["questions"],
)


@router.post("", response_model=DocumentationAnswer)
async def ask_question(
    request: AskQuestionRequest,
) -> DocumentationAnswer:
    if request.specification_id not in SPEC_STORE:
        raise HTTPException(
            status_code=404,
            detail="Specification not found.",
        )

    return await answer_documentation_question(
        request.specification_id,
        request.question,
    )