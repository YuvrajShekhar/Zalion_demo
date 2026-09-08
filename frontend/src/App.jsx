import { useEffect, useState, useCallback } from "react";
import { api } from "./api";
import RFQPanel from "./components/RFQPanel";
import QuoteForm from "./components/QuoteForm";
import Comparison from "./components/Comparison";

export default function App() {
  const [rfqs, setRfqs] = useState([]);
  const [activeRfq, setActiveRfq] = useState(null);
  const [comparison, setComparison] = useState(null);

  const loadRfqs = useCallback(async () => {
    const data = await api.listRfqs();
    setRfqs(data);
    return data;
  }, []);

  const loadComparison = useCallback(async (rfqId) => {
    const data = await api.getComparison(rfqId);
    setComparison(data);
  }, []);

  useEffect(() => {
    loadRfqs();
  }, [loadRfqs]);

  useEffect(() => {
    if (activeRfq) loadComparison(activeRfq.id);
  }, [activeRfq, loadComparison]);

  const handleCreated = async (created) => {
    const updated = await loadRfqs();
    const match = updated.find((r) => r.id === created.id);
    setActiveRfq(match);
  };

  return (
    <div className="shell">
      <div className="masthead">
        <h1>QuoteCompare</h1>
        <span className="tag">supplier quote scoring - no LLM, all deterministic</span>
      </div>

      <div className="layout">
        <div>
          <RFQPanel rfqs={rfqs} activeRfq={activeRfq} onSelect={setActiveRfq} onCreated={handleCreated} />
        </div>

        <div>
          {!activeRfq && <div className="panel"><div className="empty">Select or create an RFQ to begin</div></div>}
          {activeRfq && (
            <>
              <QuoteForm rfqId={activeRfq.id} onAdded={() => loadComparison(activeRfq.id)} />
              {comparison && <Comparison rfq={comparison.rfq} rankedQuotes={comparison.ranked_quotes} />}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
