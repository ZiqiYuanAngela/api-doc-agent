export interface SpecificationSummary {
  id: string;
  title: string;
  version: string | null;
  openapi_version: string;
  endpoint_count: number;
}

export interface EndpointReference {
  method: string;
  path: string;
  operation_id?: string | null;
}

export interface DocumentationAnswer {
  answer: string;
  endpoint?: EndpointReference | null;
  required_parameters: string[];
  optional_parameters: string[];
  request_example?: Record<string, unknown> | null;
  curl_example?: string | null;
  warnings: string[];
}

export interface ValidationError {
  path: string;
  message: string;
  validator?: string | null;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}