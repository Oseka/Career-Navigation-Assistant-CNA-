import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'

import App from './App'

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <App />
    </MemoryRouter>,
  )
}

describe('App shell', () => {
  it('renders the layout with header, primary navigation, and footer', () => {
    renderAt('/')

    expect(screen.getByRole('banner')).toBeInTheDocument()
    expect(screen.getByRole('navigation', { name: 'Primary' })).toBeInTheDocument()
    expect(screen.getByRole('contentinfo')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Dashboard' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Careers' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Assessment' })).toBeInTheDocument()
  })

  it('renders the home page at the root route', () => {
    renderAt('/')

    expect(screen.getByRole('heading', { name: /discover technology careers that fit you/i }))
      .toBeInTheDocument()
    expect(screen.getByRole('link', { name: /start the assessment/i })).toBeInTheDocument()
  })

  it('renders placeholder pages for planned routes', () => {
    renderAt('/careers')

    expect(screen.getByRole('heading', { name: 'Career catalogue' })).toBeInTheDocument()
    expect(screen.getByText(/planned — increment i4/i)).toBeInTheDocument()
  })

  it('renders the not-found page for unknown routes', () => {
    renderAt('/this-does-not-exist')

    expect(screen.getByRole('heading', { name: /page not found/i })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /back to home/i })).toBeInTheDocument()
  })
})
