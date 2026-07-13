from datetime import datetime
from pydantic import BaseModel, Field

class ApiSpecification(BaseModel):
    """
    Represents the API specification for a given endpoint.
    """
    id: str = Field(..., description="The unique identifier for the API specification.")
    title: str | None = Field(default=None, description="The title of the API specification.")
    version: str = Field(..., description="The version of the API specification.")
    raw_spec: dict = Field(default_factory=dict, description="A dictionary of specification for the API call.")
    openapi_version: str = Field(..., description="The OpenAPI version.")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the specification was last updated.")

    class Config:
        orm_mode = True
