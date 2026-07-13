┌─────────────────────┐
│ Next.js UI          │
│                     │
│ Upload spec         │
│ Ask questions       │
│ Validate JSON       │
└──────────┬──────────┘
           │ REST
           ▼
┌────────────────────────────┐
│ FastAPI                    │
│                            │
│ Upload API                 │
│ Question API               │
│ Validation API             │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ OpenAPI Service            │
│                            │
│ Parse JSON/YAML            │
│ Resolve references         │
│ Build endpoint index       │
│ Extract schemas            │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Documentation Agent        │
│                            │
│ Chooses deterministic      │
│ tools based on question    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│ Agent Tools                │
│                            │
│ list_endpoints             │
│ search_endpoints           │
│ get_endpoint_details       │
│ generate_request_example   │
│ validate_request           │
└────────────────────────────┘
