import { useState } from "react";
import { api } from "../api";

const empty = {
  supplier_name: "",
  price_per_unit: "",
  lead_time_days: "",
  min_order_quantity: "",
  payment_terms: "",
};

export default function QuoteForm({ rfqId, onAdded }) {
  const [form, setForm] = useState(empty);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api.addQuote(rfqId, {
        supplier_name: form.supplier_name,
        price_per_unit: Number(form.price_per_unit),
        lead_time_days: Number(form.lead_time_days),
        min_order_quantity: Number(form.min_order_quantity),
        payment_terms: form.payment_terms,
      });
      setForm(empty);
      onAdded();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="panel">
      <h2>Add Supplier Quote</h2>
      <form onSubmit={submit}>
        <label>Supplier name</label>
        <input value={form.supplier_name} onChange={update("supplier_name")} required placeholder="e.g. Acme Fasteners" />

        <label>Price / unit (EUR)</label>
        <input type="number" step="0.01" min="0.01" value={form.price_per_unit} onChange={update("price_per_unit")} required />

        <label>Lead time (days)</label>
        <input type="number" min="1" value={form.lead_time_days} onChange={update("lead_time_days")} required />

        <label>Minimum order quantity</label>
        <input type="number" min="1" value={form.min_order_quantity} onChange={update("min_order_quantity")} required />

        <label>Payment terms</label>
        <input value={form.payment_terms} onChange={update("payment_terms")} required placeholder="e.g. Net 30" />

        <button type="submit" disabled={busy}>{busy ? "Adding…" : "Add Quote"}</button>
        {error && <div className="error">{error}</div>}
      </form>
    </div>
  );
}
