import type { SpecificationSummary as Specification } from "@/lib/types";

interface SpecificationSummaryProps {
  specification: Specification;
}

export default function SpecificationSummary({
  specification,
}: SpecificationSummaryProps) {
  return (
    <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold text-emerald-700">
            Specification loaded
          </p>

          <h2 className="mt-1 text-xl font-semibold text-slate-900">
            {specification.title}
          </h2>

          <p className="mt-2 text-sm text-slate-600">
            You can now ask questions or validate request payloads.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <SummaryValue
            label="API version"
            value={specification.version ?? "Not specified"}
          />

          <SummaryValue
            label="OpenAPI"
            value={specification.openapi_version}
          />

          <SummaryValue
            label="Endpoints"
            value={String(specification.endpoint_count)}
          />

          <SummaryValue
            label="Specification ID"
            value={`${specification.id.slice(0, 8)}...`}
          />
        </div>
      </div>
    </section>
  );
}

interface SummaryValueProps {
  label: string;
  value: string;
}

function SummaryValue({
  label,
  value,
}: SummaryValueProps) {
  return (
    <div className="rounded-lg bg-white px-3 py-2">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-1 max-w-36 truncate font-medium text-slate-900">
        {value}
      </p>
    </div>
  );
}