"use client";

import { FormEvent, useState } from "react";

import { askDocumentationQuestion } from "@/lib/api";
import type { DocumentationAnswer } from "@/lib/types";

interface QuestionFormProps {
  specificationId: string;
  onAnswer: (answer: DocumentationAnswer) => void;
}

export default function QuestionForm({
  specificationId,
  onAnswer,
}: QuestionFormProps) {
  const [question, setQuestion] = useState("");
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (trimmedQuestion.length < 3) {
      setError("Enter a question containing at least three characters.");
      return;
    }

    setIsAsking(true);
    setError(null);

    try {
      const answer = await askDocumentationQuestion(
        specificationId,
        trimmedQuestion,
      );

      onAnswer(answer);
    } catch (questionError) {
      setError(
        questionError instanceof Error
          ? questionError.message
          : "The question could not be processed.",
      );
    } finally {
      setIsAsking(false);
    }
  }

  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-5">
        <p className="text-sm font-semibold text-blue-600">
          Step 2
        </p>

        <h2 className="mt-1 text-xl font-semibold text-slate-900">
          Ask about the API
        </h2>

        <p className="mt-2 text-sm text-slate-600">
          Ask which endpoint to use, which fields are required, or
          request an example.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <label
          htmlFor="documentation-question"
          className="block text-sm font-medium text-slate-700"
        >
          Developer question
        </label>

        <textarea
          id="documentation-question"
          value={question}
          onChange={(event) => {
            setQuestion(event.target.value);
            setError(null);
          }}
          rows={4}
          placeholder="For example: How do I create a customer?"
          className="w-full resize-y rounded-lg border border-slate-300 px-3 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />

        <div className="flex flex-wrap gap-2">
          {[
            "How do I create a customer?",
            "Which endpoint gets an order by ID?",
            "Generate a request example.",
          ].map((example) => (
            <button
              key={example}
              type="button"
              onClick={() => setQuestion(example)}
              className="rounded-full border border-slate-300 px-3 py-1 text-xs text-slate-600 hover:bg-slate-50"
            >
              {example}
            </button>
          ))}
        </div>

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
          disabled={isAsking}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isAsking ? "Analyzing..." : "Ask agent"}
        </button>
      </form>
    </section>
  );
}