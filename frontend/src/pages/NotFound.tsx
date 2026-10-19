import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <section aria-labelledby="not-found-heading" className="mx-auto max-w-6xl px-4 py-16">
      <h1 id="not-found-heading" className="text-3xl font-bold tracking-tight">
        Page not found
      </h1>
      <p className="mt-4 max-w-2xl text-slate-600">
        The page you are looking for does not exist or has not been built yet.
      </p>
      <Link
        to="/"
        className="mt-6 inline-block rounded-lg bg-sky-700 px-5 py-2.5 font-medium text-white transition-colors hover:bg-sky-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-700"
      >
        Back to home
      </Link>
    </section>
  )
}
