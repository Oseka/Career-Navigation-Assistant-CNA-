import { Link } from 'react-router-dom'

const highlights = [
  {
    title: 'Assess your interests',
    description:
      'A structured questionnaire covering nine technology areas, from software development to cybersecurity.',
  },
  {
    title: 'See why careers fit',
    description:
      'Transparent, factor-level explanations — matched interests, matched skills, and development areas.',
  },
  {
    title: 'Follow a learning roadmap',
    description:
      'Staged milestones with resources and portfolio projects, so you always know the next practical step.',
  },
]

export function Home() {
  return (
    <section aria-labelledby="home-heading" className="mx-auto max-w-6xl px-4 py-16">
      <h1 id="home-heading" className="max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
        Discover technology careers that fit you
      </h1>
      <p className="mt-4 max-w-2xl text-lg text-slate-600">
        CNA helps Computer Science students explore suitable career paths, understand the skills they
        require, and follow a personalised plan to prepare for them.
      </p>

      <div className="mt-8 flex flex-wrap gap-4">
        <Link
          to="/assessment"
          className="rounded-lg bg-sky-700 px-5 py-2.5 font-medium text-white transition-colors hover:bg-sky-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-700"
        >
          Start the assessment
        </Link>
        <Link
          to="/careers"
          className="rounded-lg border border-slate-300 bg-white px-5 py-2.5 font-medium text-slate-800 transition-colors hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-700"
        >
          Browse careers
        </Link>
      </div>

      <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {highlights.map((item) => (
          <div key={item.title} className="rounded-xl border border-slate-200 bg-white p-6">
            <h2 className="text-lg font-semibold">{item.title}</h2>
            <p className="mt-2 text-sm text-slate-600">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
