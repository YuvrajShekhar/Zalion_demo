import { useState } from "react";
import { api } from "../api";

const empty = {
  title: "",
  quantity_needed: "",
  target_price_per_unit: "",
  deadline_days: "",
  preferred_payment_terms: "Net 30",
};

export default function RFQPanel({ rfqs, activeRfq, onSelect, onCreated }) {
  const [form, setForm] = useState(empty);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const created = await api.createRfq({
        title: form.title,
        quantity_needed: Number(form.quantity_needed),
        target_price_per_unit: Number(form.target_price_per_unit),
        deadline_days: Number(form.deadline_days),
        preferred_payment_terms: form.preferred_payment_terms,
      });
      setForm(empty);
      onCreated(created);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div className="panel">
        <h2>New RFQ</h2>
        <form onSubmit={submit}>
          <label>Title</label>
          <input value={form.title} onChange={update("title")} required placeholder="e.g. Steel bolts Q3" />

          <label>Quantity needed</label>
          <input type="number" min="1" value={form.quantity_needed} onChange={update("quantity_needed")} required />

          <label>Target price / unit (EUR)</label>
          <input type="number" step="0.01" min="0.01" value={form.target_price_per_unit} onChange={update("target_price_per_unit")} required />

          <label>Deadline (days)</label>
          <input type="number" min="1" value={form.deadline_days} onChange={update("deadline_days")} required />

          <label>Preferred payment terms</label>
          <input value={form.preferred_payment_terms} onChange={update("preferred_payment_terms")} required />

          <button type="submit" disabled={busy}>{busy ? "Creating…" : "Create RFQ"}</button>
          {error && <div className="error">{error}</div>}
        </form>
      </div>

      <div className="panel">
        <h2>Open RFQs</h2>
        {rfqs.length === 0 && <div className="empty">No RFQs yet</div>}
        <div className="rfq-list">
          {rfqs.map((r) => (
            <div
              key={r.id}
              className={`rfq-row ${activeRfq?.id === r.id ? "active" : ""}`}
              onClick={() => onSelect(r)}
            >
              <span>{r.title}</span>
              <span className="n">#{r.id}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
