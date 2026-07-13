"use client";

import { useState } from "react";

import DocumentationAnswerCard from "@/components/DocumentationAnswerCard";
import QuestionForm from "@/components/QuestionForm";
import RequestValidator from "@/components/RequestValidator";
import SpecificationSummary from "@/components/SpecificationSummary";
import SpecUploader from "@/components/SpecUploader";
import type {
  DocumentationAnswer,
  SpecificationSummary as Specification,
} from "@/lib/types";

export default function ApiDocumentationApp() {
  const [specification, setSpecification] =
    useState<Specification | null>(null);

  const [answer, setAnswer] =
    useState<DocumentationAnswer | null>(null);

  function handleUploaded(newSpecification: Specification): void {
    setSpecification(newSpecification);
    setAnswer(null);
  }

  return (
    <div className="space-y-6">
      <SpecUploader onUploaded={handleUploaded} />

      {specification ? (
        <>
          <SpecificationSummary specification={specification} />

          <div className="grid gap-6 xl:grid-cols-2">
            <div className="space-y-6">
              <QuestionForm
                specificationId={specification.id}
                onAnswer={setAnswer}
              />

              {answer ? (
                <DocumentationAnswerCard answer={answer} />
              ) : null}
            </div>

            <RequestValidator specificationId={specification.id} />
          </div>
        </>
      ) : (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="font-semibold text-slate-800">
            Upload a specification to begin
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            The question and validation tools will appear after your
            API specification is loaded.
          </p>
        </div>
      )}
    </div>
  );
}