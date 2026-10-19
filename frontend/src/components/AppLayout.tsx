import { Link, NavLink, Outlet } from 'react-router-dom'

const navLinks = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/careers', label: 'Careers' },
  { to: '/assessment', label: 'Assessment' },
]

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  [
    'rounded-md px-3 py-1.5 text-sm font-medium transition-colors',
    isActive ? 'bg-sky-100 text-sky-800' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900',
  ].join(' ')

export function AppLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-x-6 gap-y-2 px-4 py-3">
          <Link to="/" className="text-lg font-bold tracking-tight text-sky-700">
            CNA
          </Link>
          <nav aria-label="Primary" className="flex flex-wrap items-center gap-1">
            {navLinks.map((link) => (
              <NavLink key={link.to} to={link.to} className={navLinkClass}>
                {link.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="flex-1">
        <Outlet />
      </main>

      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-3 text-sm text-slate-500">
          Career Navigation Assistant — guidance for exploration, not a verdict on suitability.
        </div>
      </footer>
    </div>
  )
}
