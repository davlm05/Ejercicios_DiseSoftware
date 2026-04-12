import { useState, useEffect } from 'react';
import { fetchTours } from '../api';

export default function TourList() {
  const [tours, setTours] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTours()
      .then(setTours)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="text-gray-400">Cargando tours...</p>;
  if (error) return <p className="text-red-400">Error: {error}</p>;

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {tours.length === 0 && (
        <p className="col-span-2 text-gray-500">No hay tours disponibles aun.</p>
      )}
      {tours.map((tour) => (
        <div
          key={tour.id}
          className="rounded-lg border border-sky-700/30 bg-sky-950/40 p-5 text-left"
        >
          <h3 className="text-lg font-semibold text-sky-300">{tour.name}</h3>
          <p className="mt-1 text-sm text-gray-400">{tour.description}</p>
          <div className="mt-3 flex flex-wrap gap-3 text-sm text-gray-300">
            <span>Ubicacion: {tour.location}</span>
            <span>Precio: ${tour.price}</span>
            <span>Capacidad: {tour.maxCapacity}</span>
            <span>Guia: {tour.guideName}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
