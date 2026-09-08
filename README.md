# QuoteCompare

Supplier quote intake and scoring engine for procurement RFQs. Built as a
small proof-of-concept for a FastAPI + React + Postgres stack.

**What it does:** create an RFQ (target price, quantity, deadline, preferred
payment terms), log supplier quotes against it, and get a ranked comparison
with a transparent 0-100 score breakdown (price / lead time / compliance)
and plain-language flags for anything that misses the RFQ terms.

The scoring is deliberately **not** an LLM call - see `backend/app/scoring.py`.
It's a small, deterministic, fully testable function. The intent is that this
is the kind of business-logic "tool" an LLM agent orchestrator would call
rather than something you'd want an LLM to eyeball - decisions with money and
deadlines attached should be reproducible and explainable, and rule-based
scoring is cheap, fast, and has zero hallucination risk. An agent layer could
sit on top of this later (e.g. parsing free-text supplier emails into the
structured quote fields this API expects) without touching the scoring logic
itself.

## Stack

- **Backend:** FastAPI, SQLAlchemy, Postgres (SQLite fallback for local dev)
- **Frontend:** React + Vite, no UI framework - plain CSS
- **Deploy target:** Railway

## URL

Live : `https://superb-delight-production-c936.up.railway.app/`

## API

| Method | Path                        | Description                          |
|--------|-----------------------------|---------------------------------------|
| POST   | `/rfqs`                     | Create an RFQ                        |
| GET    | `/rfqs`                     | List RFQs                            |
| GET    | `/rfqs/{id}`                | Get one RFQ                          |
| POST   | `/rfqs/{id}/quotes`         | Add a supplier quote to an RFQ       |
| GET    | `/rfqs/{id}/quotes`         | List quotes for an RFQ               |
| GET    | `/rfqs/{id}/comparison`     | Ranked, scored comparison of quotes  |

## Tests

```bash
cd backend
source venv/bin/activate
pip install pytest
pytest
```
