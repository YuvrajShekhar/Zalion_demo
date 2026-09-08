export default function Comparison({ rfq, rankedQuotes }) {
  return (
    <div className="panel">
      <h2>Comparison - {rfq.title}</h2>

      <div className="rfq-summary">
        <div className="stat">
          <div className="v">{rfq.quantity_needed}</div>
          <div className="k">Qty needed</div>
        </div>
        <div className="stat">
          <div className="v">€{rfq.target_price_per_unit.toFixed(2)}</div>
          <div className="k">Target / unit</div>
        </div>
        <div className="stat">
          <div className="v">{rfq.deadline_days}d</div>
          <div className="k">Deadline</div>
        </div>
        <div className="stat">
          <div className="v">{rfq.preferred_payment_terms}</div>
          <div className="k">Preferred terms</div>
        </div>
      </div>

      {rankedQuotes.length === 0 && <div className="empty">No quotes submitted yet</div>}

      {rankedQuotes.map((sq, i) => (
        <div className="quote-card" key={sq.quote.id}>
          <div className="quote-head">
            <div>
              <span className="rank">#{i + 1}</span>
              <span className="name">{sq.quote.supplier_name}</span>
            </div>
            <div className="score">{sq.total_score}</div>
          </div>
          <div className="quote-body">
            <div className="bars">
              <ScoreBar label="Price" value={sq.price_score} max={40} />
              <ScoreBar label="Lead time" value={sq.lead_time_score} max={30} />
              <ScoreBar label="Compliance" value={sq.compliance_score} max={30} />
            </div>
            <div className="details">
              <span>€{sq.quote.price_per_unit.toFixed(2)}/unit</span>
              <span>{sq.quote.lead_time_days}d lead time</span>
              <span>MOQ {sq.quote.min_order_quantity}</span>
              <span>{sq.quote.payment_terms}</span>
            </div>
            <div className="flags">
              {sq.flags.length === 0 ? (
                <span className="clean-pill">Meets all RFQ terms</span>
              ) : (
                sq.flags.map((f, idx) => (
                  <span className="flag-pill" key={idx}>{f}</span>
                ))
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

function ScoreBar({ label, value, max }) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100));
  return (
    <div className="bar-item">
      <div className="label">
        <span>{label}</span>
        <span>{value}/{max}</span>
      </div>
      <div className="bar-track">
        <div className="bar-fill" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
