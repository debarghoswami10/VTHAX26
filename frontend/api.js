// api.js
const API_BASE = "http://localhost:8000"; // change in prod

export async function classify(query) {
  const r = await fetch(`${API_BASE}/classify`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ query })
  });
  if (!r.ok) throw new Error("classify failed");
  return (await r.json()).category; // e.g. "repairs"
}

export async function fetchProviders(category) {
  const url = `${API_BASE}/providers?category=${encodeURIComponent(category)}`;
  const r = await fetch(url);
  if (!r.ok) throw new Error("providers failed");
  return (await r.json()).providers;
}

export async function createBooking(payload) {
  const r = await fetch(`${API_BASE}/bookings/new`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error("booking failed");
  return (await r.json()).booking;
}
