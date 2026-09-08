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

## Run locally

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Runs against a local `quotecompare.db` SQLite file by default - no Postgres
needed for local dev. Set `DATABASE_URL` to point at Postgres instead
(Railway injects this automatically when you add a Postgres service).

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Opens on http://localhost:5173, talking to the backend on
`http://localhost:8000` by default. Override with a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Deploy to Railway

1. Push this repo to GitHub.
2. Create a new Railway project, add a **Postgres** service.
3. Add a second service from the repo, root directory `backend`.
   Railway auto-injects `DATABASE_URL` from the Postgres service - no
   extra config needed. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add a third service from the repo, root directory `frontend`.
   Build command: `npm install && npm run build`.
   Start command: `npm run preview`.
   Set `VITE_API_URL` to the backend service's public Railway URL.

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

Covers the scoring engine's core cases: on-budget vs over-budget pricing,
lead time within/outside deadline, MOQ and payment-term compliance.
