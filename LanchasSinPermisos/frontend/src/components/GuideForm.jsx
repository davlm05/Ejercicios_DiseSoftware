import { useState } from 'react';
import { createGuide } from '../api';

export default function GuideForm({ onCreated }) {
  const [form, setForm] = useState({ name: '', phone: '', zone: '', experience: '0' });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createGuide({ ...form, experience: parseInt(form.experience) });
    setForm({ name: '', phone: '', zone: '', experience: '0' });
    onCreated();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <div className="grid gap-3 md:grid-cols-2">
        <input name="name" placeholder="Nombre completo" value={form.name} onChange={handleChange} required className="rounded border border-emerald-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="phone" placeholder="Telefono" value={form.phone} onChange={handleChange} required className="rounded border border-emerald-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="zone" placeholder="Zona (ej. Bahia Drake)" value={form.zone} onChange={handleChange} required className="rounded border border-emerald-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
        <input name="experience" type="number" placeholder="Anios de experiencia" value={form.experience} onChange={handleChange} className="rounded border border-emerald-700/40 bg-gray-900 px-3 py-2 text-white placeholder-gray-500" />
      </div>
      <button type="submit" className="rounded bg-emerald-600 px-5 py-2 font-semibold text-white hover:bg-emerald-500">Registrar Guia</button>
    </form>
  );
}
