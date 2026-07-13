"use client";

import { FormEvent, useRef, useState } from "react";

import { uploadSpecification } from "@/lib/api";
import type { SpecificationSummary } from "@/lib/types";

interface SpecUploaderProps {
  onUploaded: (specification: SpecificationSummary) => void;
}

export default function SpecUploader({
  onUploaded,
}: SpecUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    if (!selectedFile) {
      setError("Choose an OpenAPI JSON or YAML file.");
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const specification = await uploadSpecification(selectedFile);
      onUploaded(specification);

      setSelectedFile(null);

      if (inputRef.current) {
        inputRef.current.value = "";
      }
    } catch (uploadError) {
      setError(
        uploadError instanceof Error
          ? uploadError.message
          : "The specification could not be uploaded.",
      );
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <p className="text-sm font-semibold text-blue-600">
          Step 1
        </p>

        <h2 className="mt-1 text-xl font-semibold text-slate-900">
          Upload an OpenAPI specification
        </h2>

        <p className="mt-2 text-sm text-slate-600">
          Supported file types: JSON, YAML, and YML.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          ref={inputRef}
          type="file"
          accept=".json,.yaml,.yml,application/json,text/yaml"
          onChange={(event) => {
            setSelectedFile(event.target.files?.[0] ?? null);
            setError(null);
          }}
          className="block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-700 file:mr-4 file:rounded-md file:border-0 file:bg-slate-100 file:px-4 file:py-2 file:text-sm file:font-medium file:text-slate-700 hover:file:bg-slate-200"
        />

        {selectedFile ? (
          <p className="text-sm text-slate-600">
            Selected:{" "}
            <span className="font-medium">{selectedFile.name}</span>
          </p>
        ) : null}

        {error ? (
          <p
            role="alert"
            className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700"
          >
            {error}
          </p>
        ) : null}

        <button
          type="submit"
          disabled={isUploading || !selectedFile}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isUploading ? "Uploading..." : "Upload specification"}
        </button>
      </form>
    </section>
  );
}