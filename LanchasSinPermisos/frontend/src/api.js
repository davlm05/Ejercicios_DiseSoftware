const TOURS_API = 'http://localhost:8081';
const GUIDES_API = 'http://localhost:8082';

export async function fetchTours() {
  const res = await fetch(`${TOURS_API}/tours`);
  if (!res.ok) throw new Error('Error fetching tours');
  return res.json();
}

export async function createTour(tour) {
  const res = await fetch(`${TOURS_API}/tours`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(tour),
  });
  if (!res.ok) throw new Error('Error creating tour');
  return res.json();
}

export async function fetchGuides() {
  const res = await fetch(`${GUIDES_API}/guides`);
  if (!res.ok) throw new Error('Error fetching guides');
  return res.json();
}

export async function createGuide(guide) {
  const res = await fetch(`${GUIDES_API}/guides`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(guide),
  });
  if (!res.ok) throw new Error('Error creating guide');
  return res.json();
}
