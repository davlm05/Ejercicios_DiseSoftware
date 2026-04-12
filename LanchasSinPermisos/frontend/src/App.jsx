import { useState, useCallback } from 'react';
import TourList from './components/TourList';
import TourForm from './components/TourForm';
import GuideList from './components/GuideList';
import GuideForm from './components/GuideForm';

function App() {
  const [tab, setTab] = useState('tours');
  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = useCallback(() => setRefreshKey((k) => k + 1), []);

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 bg-gray-950/80 px-6 py-4">
        <h1 className="text-2xl font-bold text-sky-400">Lanchas Sin Permisos</h1>
        <p className="text-sm text-gray-400">Tours en lancha por guias locales de la comunidad</p>
      </header>

      <nav className="flex gap-2 border-b border-gray-800 px-6 py-3">
        <button onClick={() => setTab('tours')} className={`rounded px-4 py-2 text-sm font-medium ${tab === 'tours' ? 'bg-sky-600 text-white' : 'text-gray-400 hover:text-white'}`}>Tours</button>
        <button onClick={() => setTab('guides')} className={`rounded px-4 py-2 text-sm font-medium ${tab === 'guides' ? 'bg-emerald-600 text-white' : 'text-gray-400 hover:text-white'}`}>Guias</button>
      </nav>

      <main className="mx-auto max-w-4xl p-6">
        {tab === 'tours' && (
          <div className="space-y-6">
            <section>
              <h2 className="mb-4 text-xl font-semibold text-sky-300">Crear nuevo tour</h2>
              <TourForm onCreated={refresh} />
            </section>
            <section>
              <h2 className="mb-4 text-xl font-semibold text-sky-300">Tours disponibles</h2>
              <TourList key={refreshKey} />
            </section>
          </div>
        )}
        {tab === 'guides' && (
          <div className="space-y-6">
            <section>
              <h2 className="mb-4 text-xl font-semibold text-emerald-300">Registrar nuevo guia</h2>
              <GuideForm onCreated={refresh} />
            </section>
            <section>
              <h2 className="mb-4 text-xl font-semibold text-emerald-300">Guias activos</h2>
              <GuideList key={refreshKey} />
            </section>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
