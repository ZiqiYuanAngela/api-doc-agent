from agents import Agent, Runner

from app.agents.tools import (
    generate_request_example,
    get_endpoint_details,
    list_endpoints,
    search_endpoints,
    validate_request,
)
from app.models.question import DocumentationAnswer


documentation_agent = Agent(
    name="API Documentation Agent",
    instructions="""
You answer developer questions about an uploaded OpenAPI specification.

Rules:
1. Always use tools before answering questions about the API.
2. Never invent endpoints, parameters, fields, schemas, or status codes.
3. Use search_endpoints to find relevant operations.
4. Use get_endpoint_details before explaining an endpoint.
5. Use generate_request_example when the user asks for a JSON example.
6. Use validate_request only when the user provides a request payload.
7. Clearly distinguish required and optional parameters.
8. Always mention the HTTP method and path.
9. If the specification does not contain enough information, say so.
10. Return only information supported by tool results.
""",
    tools=[
        list_endpoints,
        search_endpoints,
        get_endpoint_details,
        generate_request_example,
        validate_request,
    ],
    output_type=DocumentationAnswer,
)


async def answer_documentation_question(
    specification_id: str,
    question: str,
) -> DocumentationAnswer:
    prompt = f"""
The uploaded OpenAPI specification ID is:

{specification_id}

Answer this developer question:

{question}
"""

    result = await Runner.run(
        documentation_agent,
        prompt,
    )

    return result.final_output