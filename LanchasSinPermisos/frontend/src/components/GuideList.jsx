import { useState, useEffect } from 'react';
import { fetchGuides } from '../api';

export default function GuideList() {
  const [guides, setGuides] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGuides()
      .then(setGuides)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-400">Cargando guias...</p>;
  if (error) return <p className="text-red-400">Error: {error}</p>;

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {guides.length === 0 && (
        <p className="col-span-2 text-gray-500">No hay guias registrados aun.</p>
      )}
      {guides.map((guide) => (
        <div key={guide.id} className="rounded-lg border border-emerald-700/30 bg-emerald-950/40 p-5 text-left">
          <h3 className="text-lg font-semibold text-emerald-300">{guide.name}</h3>
          <div className="mt-2 flex flex-wrap gap-3 text-sm text-gray-300">
            <span>Zona: {guide.zone}</span>
            <span>Telefono: {guide.phone}</span>
            <span>Experiencia: {guide.experience} anios</span>
          </div>
        </div>
      ))}
    </div>
  );
}
