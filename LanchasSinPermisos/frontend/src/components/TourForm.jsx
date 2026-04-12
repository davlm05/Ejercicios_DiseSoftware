import { useState } from 'react';
import { createTour } from '../api';

export default function TourForm({ onCreated }) {
  const [form, setForm] = useState({
    name: '',
    location: '',
    price: '',
    guideName: '',
    description: '',
    maxCapacity: '10',
  });

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createTour({
      ...form,
      price: parseFloat(form.price),
      maxCapacity: parseInt(form.maxCapacity),
    });
    setForm({ name: '', location: '', price: '', guideName: '', description: '', maxCapacity: '10' });
    onCreated();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input name="name" placeholder="Nombre del tour" value={form.name} onChange={handleChange} required className="rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="location" placeholder="Ubicacion (ej. Playa Hermosa)" value={form.location} onChange={handleChange} required className="rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="price" type="number" step="0.01" placeholder="Precio ($)" value={form.price} onChange={handleChange} required className="rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="guideName" placeholder="Nombre del guia" value={form.guideName} onChange={handleChange} required className="rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="maxCapacity" type="number" placeholder="Capacidad maxima" value={form.maxCapacity} onChange={handleChange} className="rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
      </div>
      <textarea name="description" placeholder="Descripcion del tour" value={form.description} onChange={handleChange} rows={2} className="w-full rounded border border-sky-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
      <button type="submit" className="rounded bg-sky-600 px-5 py-2 font-semibold text-white hover:bg-sky-500">Crear Tour</button>
    </form>
  );
}
