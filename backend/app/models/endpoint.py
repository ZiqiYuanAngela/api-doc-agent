from typing import Any
from pydantic import BaseModel, Field

class ApiParameter(BaseModel):
    """
    Represents a parameter for an API endpoint.
    """
    name: str = Field(..., description="The name of the parameter.")
    location: str = Field(..., alias="in", description="The location of the parameter (e.g., query, path, header).")
    required: bool = Field(default=False, description="Indicates if the parameter is required.")
    schema: dict[str, Any] = Field(default_factory=dict, alias="schema", description="A dictionary representing the schema of the parameter.")

class ApiEndpoint(BaseModel):
    operation_id: str | None = Field(default=None, description="The unique identifier for the API operation.")
    method: str = Field(..., description="The HTTP method for the API endpoint (e.g., GET, POST).")
    path: str = Field(..., description="The path of the API endpoint.")
    summary: str | None = Field(default=None, description="A brief summary of the API endpoint.")
    description: str | None = Field(default=None, description="A detailed description of the API endpoint.")
    parameters: list[ApiParameter] = Field(default_factory=list, description="A list of parameters for the API endpoint.")
    request_body: dict[str, Any] | None = Field(default=None, alias="requestBody", description="A dictionary representing the request body for the API endpoint.")
    responses: dict[str, Any] = Field(default_factory=dict, description="A dictionary representing the responses for the API endpoint, keyed by status code.")
    tags: list[str] = Field(default_factory=list, description="A list of tags associated with the API endpoint.")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True