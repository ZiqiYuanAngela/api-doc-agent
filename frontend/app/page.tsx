import ApiDocumentationApp from "@/components/ApiDocumentationApp";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-8">
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-600">
            AI developer tool
          </p>

          <h1 className="mt-3 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
            API Documentation Agent
          </h1>

          <p className="mt-3 max-w-3xl text-base leading-7 text-slate-600">
            Upload an OpenAPI specification, ask natural-language
            questions, generate request examples, and validate JSON
            payloads against documented schemas.
          </p>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        <ApiDocumentationApp />
      </div>
    </main>
  );
}