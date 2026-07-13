"use client";

import { FormEvent, useState } from "react";

import { validateApiRequest } from "@/lib/api";
import type { ValidationResult } from "@/lib/types";

interface RequestValidatorProps {
  specificationId: string;
}

const INITIAL_PAYLOAD = `{
  "email": "customer@example.com"
}`;

export default function RequestValidator({
  specificationId,
}: RequestValidatorProps) {
  const [method, setMethod] = useState("POST");
  const [path, setPath] = useState("");
  const [payloadText, setPayloadText] = useState(INITIAL_PAYLOAD);
  const [result, setResult] = useState<ValidationResult | null>(
    null,
  );
  const [error, setError] = useState<string | null>(null);
  const [isValidating, setIsValidating] = useState(false);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (!path.trim()) {
      setError("Enter an endpoint path.");
      return;
    }

    let parsedPayload: unknown;

    try {
      parsedPayload = JSON.parse(payloadText);
    } catch {
      setError("The request payload is not valid JSON.");
      setResult(null);
      return;
    }

    if (
      typeof parsedPayload !== "object" ||
      parsedPayload === null ||
      Array.isArray(parsedPayload)
    ) {
      setError("The request payload must be a JSON object.");
      setResult(null);
      return;
    }

    setIsValidating(true);
    setError(null);
    setResult(null);

    try {
      const validationResult = await validateApiRequest({
        specificationId,
        method,
        path: path.trim(),
        payload: parsedPayload as Record<string, unknown>,
      });

      setResult(validationResult);
    } catch (validationError) {
      setError(
        validationError instanceof Error
          ? validationError.message
          : "The request could not be validated.",
      );
    } finally {
      setIsValidating(false);
    }
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <p className="text-sm font-semibold text-blue-600">
          Step 3
        </p>

        <h2 className="mt-1 text-xl font-semibold text-slate-900">
          Validate a request
        </h2>

        <p className="mt-2 text-sm text-slate-600">
          Validate a JSON object against an endpoint request-body
          schema.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-[140px_1fr]">
          <div>
            <label
              htmlFor="request-method"
              className="block text-sm font-medium text-slate-700"
            >
              Method
            </label>

            <select
              id="request-method"
              value={method}
              onChange={(event) => setMethod(event.target.value)}
              className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900"
            >
              {["POST", "PUT", "PATCH", "GET", "DELETE"].map(
                (option) => (
                  <option key={option}>{option}</option>
                ),
              )}
            </select>
          </div>

          <div>
            <label
              htmlFor="request-path"
              className="block text-sm font-medium text-slate-700"
            >
              Endpoint path
            </label>

            <input
              id="request-path"
              value={path}
              onChange={(event) => {
                setPath(event.target.value);
                setError(null);
              }}
              placeholder="/customers"
              className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-900 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="request-payload"
            className="block text-sm font-medium text-slate-700"
          >
            JSON payload
          </label>

          <textarea
            id="request-payload"
            value={payloadText}
            onChange={(event) => {
              setPayloadText(event.target.value);
              setError(null);
              setResult(null);
            }}
            rows={12}
            spellCheck={false}
            className="mt-2 w-full rounded-xl border border-slate-300 bg-slate-950 p-4 font-mono text-sm leading-6 text-slate-100 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        {error ? (
          <p
            role="alert"
            className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700"
          >
            {error}
          </p>
        ) : null}

        {result ? (
          <ValidationResultPanel result={result} />
        ) : null}

        <button
          type="submit"
          disabled={isValidating}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isValidating ? "Validating..." : "Validate payload"}
        </button>
      </form>
    </section>
  );
}

interface ValidationResultPanelProps {
  result: ValidationResult;
}

function ValidationResultPanel({
  result,
}: ValidationResultPanelProps) {
  if (result.valid) {
    return (
      <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4">
        <p className="font-semibold text-emerald-800">
          Valid request
        </p>

        <p className="mt-1 text-sm text-emerald-700">
          The JSON payload matches the endpoint request schema.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4">
      <p className="font-semibold text-red-800">
        Invalid request
      </p>

      <ul className="mt-3 space-y-3">
        {result.errors.map((validationError, index) => (
          <li
            key={`${validationError.path}-${validationError.message}-${index}`}
            className="text-sm text-red-700"
          >
            {validationError.path ? (
              <code className="mr-2 rounded bg-red-100 px-1.5 py-0.5">
                {validationError.path}
              </code>
            ) : null}

            {validationError.message}
          </li>
        ))}
      </ul>
    </div>
  );
}