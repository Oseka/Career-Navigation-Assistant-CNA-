import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiError, apiFetch } from './client'

afterEach(() => {
  vi.unstubAllGlobals()
})

function jsonResponse(body: unknown, status: number) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

describe('apiFetch', () => {
  it('returns parsed JSON for a successful response', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ status: 'ok' }, 200)))

    await expect(apiFetch<{ status: string }>('/api/health')).resolves.toEqual({ status: 'ok' })
  })

  it('throws ApiError carrying the error envelope fields', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(
        async () =>
          jsonResponse({ error: { code: 'NOT_FOUND', message: 'Missing', details: ['a'] } }, 404),
      ),
    )

    const error: unknown = await apiFetch('/api/nope').catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    const apiError = error as ApiError
    expect(apiError.status).toBe(404)
    expect(apiError.code).toBe('NOT_FOUND')
    expect(apiError.message).toBe('Missing')
    expect(apiError.details).toEqual(['a'])
  })

  it('falls back to a generic code when the error body is not the envelope', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => jsonResponse({ unexpected: true }, 500)))

    const error: unknown = await apiFetch('/api/broken').catch((e: unknown) => e)

    expect(error).toBeInstanceOf(ApiError)
    const apiError = error as ApiError
    expect(apiError.status).toBe(500)
    expect(apiError.code).toBe('INTERNAL')
  })

  it('adds the CSRF header and JSON content type on mutations', async () => {
    const fetchMock = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) => jsonResponse({}, 200),
    )
    vi.stubGlobal('fetch', fetchMock)

    await apiFetch('/api/things', { method: 'POST', body: JSON.stringify({ a: 1 }) })

    const init = fetchMock.mock.calls[0][1]!
    const headers = init.headers as Headers
    expect(init.method).toBe('POST')
    expect(headers.get('X-CSRF-Protection')).toBe('1')
    expect(headers.get('Content-Type')).toBe('application/json')
  })

  it('does not add the CSRF header on GET requests', async () => {
    const fetchMock = vi.fn(
      async (_input: RequestInfo | URL, _init?: RequestInit) => jsonResponse({}, 200),
    )
    vi.stubGlobal('fetch', fetchMock)

    await apiFetch('/api/things')

    const init = fetchMock.mock.calls[0][1]!
    const headers = init.headers as Headers
    expect(headers.get('X-CSRF-Protection')).toBeNull()
  })
})
