export class ApiError extends Error {
  readonly status: number
  readonly code: string
  readonly details: string[]

  constructor(status: number, code: string, message: string, details: string[] = []) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
  }
}

interface ErrorEnvelope {
  error: {
    code?: string
    message?: string
    details?: string[]
  }
}

export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const method = init.method ?? 'GET'
  const headers = new Headers(init.headers)
  if (init.body != null && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }
  // The API rejects cross-site mutations without this header (CSRF defence).
  if (method !== 'GET' && method !== 'HEAD') {
    headers.set('X-CSRF-Protection', '1')
  }

  const response = await fetch(path, { ...init, method, headers, credentials: 'same-origin' })

  if (!response.ok) {
    let code = 'INTERNAL'
    let message = `Request failed with status ${response.status}`
    let details: string[] = []
    try {
      const body = (await response.json()) as ErrorEnvelope
      if (body?.error) {
        code = body.error.code ?? code
        message = body.error.message ?? message
        details = body.error.details ?? []
      }
    } catch {
      // Non-JSON error body: keep the defaults above.
    }
    throw new ApiError(response.status, code, message, details)
  }

  if (response.status === 204) {
    return undefined as T
  }
  return (await response.json()) as T
}
