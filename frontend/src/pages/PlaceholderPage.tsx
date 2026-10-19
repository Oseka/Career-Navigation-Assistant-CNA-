interface PlaceholderPageProps {
  title: string
  increment: string
  description: string
}

export function PlaceholderPage({ title, increment, description }: PlaceholderPageProps) {
  return (
    <section aria-labelledby="placeholder-heading" className="mx-auto max-w-6xl px-4 py-16">
      <p className="text-sm font-semibold uppercase tracking-wide text-sky-700">
        Planned — increment {increment}
      </p>
      <h1 id="placeholder-heading" className="mt-2 text-3xl font-bold tracking-tight">
        {title}
      </h1>
      <p className="mt-4 max-w-2xl text-slate-600">{description}</p>
    </section>
  )
}
