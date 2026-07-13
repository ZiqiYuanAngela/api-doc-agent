import type {
  DocumentationAnswer,
  SpecificationSummary,
  ValidationResult,
} from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function parseError(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as {
      detail?: string;
      message?: string;
    };

    return (
      body.detail ??
      body.message ??
      `Request failed with status ${response.status}`
    );
  } catch {
    return `Request failed with status ${response.status}`;
  }
}

export async function uploadSpecification(
  file: File,
): Promise<SpecificationSummary> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/specifications`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      Origin: "http://localhost:3000",
    },
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as SpecificationSummary;
}

export async function askDocumentationQuestion(
  specificationId: string,
  question: string,
): Promise<DocumentationAnswer> {
  const response = await fetch(`${API_BASE_URL}/api/questions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      Origin: "http://localhost:3000",
    },
    body: JSON.stringify({
      specification_id: specificationId,
      question,
    }),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as DocumentationAnswer;
}

interface ValidateRequestInput {
  specificationId: string;
  method: string;
  path: string;
  payload: Record<string, unknown>;
}

export async function validateApiRequest(
  input: ValidateRequestInput,
): Promise<ValidationResult> {
  const response = await fetch(
    `${API_BASE_URL}/api/validation/request`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        Origin: "http://localhost:3000",
      },
      body: JSON.stringify({
        specification_id: input.specificationId,
        method: input.method,
        path: input.path,
        payload: input.payload,
      }),
    },
  );

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as ValidationResult;
}