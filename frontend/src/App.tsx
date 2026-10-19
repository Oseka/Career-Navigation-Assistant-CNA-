import { Route, Routes } from 'react-router-dom'

import { AppLayout } from './components/AppLayout'
import { Home } from './pages/Home'
import { NotFound } from './pages/NotFound'
import { PlaceholderPage } from './pages/PlaceholderPage'

export default function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Home />} />
        <Route
          path="dashboard"
          element={
            <PlaceholderPage
              title="Dashboard"
              increment="I8"
              description="Your personal career development overview: assessment status, top recommendations with reasons, followed careers, and roadmap progress."
            />
          }
        />
        <Route
          path="careers"
          element={
            <PlaceholderPage
              title="Career catalogue"
              increment="I4"
              description="Browse and search a curated catalogue of technology careers with responsibilities, required skills, and learning guidance."
            />
          }
        />
        <Route
          path="assessment"
          element={
            <PlaceholderPage
              title="Career discovery assessment"
              increment="I3"
              description="A structured questionnaire about your interests, preferred activities, and strengths across nine technology areas."
            />
          }
        />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  )
}
