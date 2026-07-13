from pydantic import BaseModel, Field
from typing import Any

class EndpointReference(BaseModel):
    """
    Represents a reference to an API endpoint.
    """
    operation_id: str | None = Field(default=None, description="The unique identifier for the API operation.")
    method: str = Field(..., description="The HTTP method for the API endpoint (e.g., GET, POST).")
    path: str = Field(..., description="The path of the API endpoint.")

class DocumentationAnswer(BaseModel):
    """
    Represents the answer to a documentation request.
    """
    endpoint: EndpointReference = Field(..., description="A reference to the API endpoint.")
    curl_example: str | None = Field(default=None, description="The cURL example for the API endpoint.")
    answer: str = Field(..., description="The answer to the documentation request.")
    required_parameters: list[str] = Field(default_factory=list, description="A list of required parameters for the API endpoint.")
    request_example: dict | None = Field(default=None, description="An example of the request body for the API endpoint.")
    warnings: list[str] = Field(default_factory=list, description="A list of warnings related to the documentation request.")

class AskQuestionRequest(BaseModel):
    specification_id: str
    question: str = Field(
        min_length=3,
        max_length=2000,
    )

class ValidateRequestBody(BaseModel):
    specification_id: str
    method: str
    path: str
    payload: dict[str, Any]