import { BrowserRouter } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold text-center text-primary-600">
            ServiceHub
          </h1>
          <p className="text-center text-gray-600 mt-4">
            On-Demand Home Services Platform
          </p>
          <div className="mt-8 p-6 bg-white rounded-lg shadow-md max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">Project Setup Complete! ✅</h2>
            <ul className="space-y-2 text-gray-700">
              <li>✅ Backend structure created</li>
              <li>✅ Frontend structure created</li>
              <li>✅ Docker Compose configured</li>
              <li>✅ Database models defined</li>
              <li>✅ TailwindCSS configured</li>
            </ul>
            <p className="mt-4 text-sm text-gray-500">
              Ready for team development! Check the README for setup instructions.
            </p>
          </div>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
