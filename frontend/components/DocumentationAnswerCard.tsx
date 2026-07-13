import type { DocumentationAnswer } from "@/lib/types";

interface DocumentationAnswerCardProps {
  answer: DocumentationAnswer;
}

export default function DocumentationAnswerCard({
  answer,
}: DocumentationAnswerCardProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold text-blue-600">
        Agent response
      </p>

      {answer.endpoint ? (
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <MethodBadge method={answer.endpoint.method} />

          <code className="rounded-md bg-slate-100 px-3 py-1.5 text-sm font-semibold text-slate-800">
            {answer.endpoint.path}
          </code>

          {answer.endpoint.operation_id ? (
            <span className="text-sm text-slate-500">
              {answer.endpoint.operation_id}
            </span>
          ) : null}
        </div>
      ) : null}

      <p className="mt-5 whitespace-pre-wrap leading-7 text-slate-700">
        {answer.answer}
      </p>

      {answer.required_parameters.length > 0 ? (
        <ParameterList
          title="Required parameters"
          parameters={answer.required_parameters}
        />
      ) : null}

      {answer.optional_parameters.length > 0 ? (
        <ParameterList
          title="Optional parameters"
          parameters={answer.optional_parameters}
        />
      ) : null}

      {answer.request_example ? (
        <CodeSection
          title="Request example"
          code={JSON.stringify(answer.request_example, null, 2)}
        />
      ) : null}

      {answer.curl_example ? (
        <CodeSection
          title="cURL example"
          code={answer.curl_example}
        />
      ) : null}

      {answer.warnings.length > 0 ? (
        <div className="mt-6 rounded-lg border border-amber-200 bg-amber-50 p-4">
          <h3 className="font-semibold text-amber-900">
            Warnings
          </h3>

          <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-amber-800">
            {answer.warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}

interface MethodBadgeProps {
  method: string;
}

function MethodBadge({ method }: MethodBadgeProps) {
  return (
    <span className="rounded-md bg-slate-900 px-2.5 py-1 text-xs font-bold uppercase tracking-wide text-white">
      {method}
    </span>
  );
}

interface ParameterListProps {
  title: string;
  parameters: string[];
}

function ParameterList({
  title,
  parameters,
}: ParameterListProps) {
  return (
    <div className="mt-6">
      <h3 className="font-semibold text-slate-900">{title}</h3>

      <div className="mt-2 flex flex-wrap gap-2">
        {parameters.map((parameter) => (
          <code
            key={parameter}
            className="rounded-md bg-slate-100 px-2.5 py-1 text-sm text-slate-700"
          >
            {parameter}
          </code>
        ))}
      </div>
    </div>
  );
}

interface CodeSectionProps {
  title: string;
  code: string;
}

function CodeSection({ title, code }: CodeSectionProps) {
  return (
    <div className="mt-6">
      <h3 className="font-semibold text-slate-900">{title}</h3>

      <pre className="mt-2 overflow-x-auto rounded-xl bg-slate-950 p-4 text-sm leading-6 text-slate-100">
        <code>{code}</code>
      </pre>
    </div>
  );
}