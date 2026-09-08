const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status}: ${body}`);
  }
  return res.json();
}

export const api = {
  listRfqs: () => request("/rfqs"),
  createRfq: (data) => request("/rfqs", { method: "POST", body: JSON.stringify(data) }),
  addQuote: (rfqId, data) =>
    request(`/rfqs/${rfqId}/quotes`, { method: "POST", body: JSON.stringify(data) }),
  getComparison: (rfqId) => request(`/rfqs/${rfqId}/comparison`),
};
