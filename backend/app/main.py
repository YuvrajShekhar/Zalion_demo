from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db
from .scoring import rank_quotes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QuoteCompare", description="Supplier quote comparison & scoring engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "QuoteCompare API"}


@app.post("/rfqs", response_model=schemas.RFQOut)
def create_rfq(rfq: schemas.RFQCreate, db: Session = Depends(get_db)):
    db_rfq = models.RFQ(**rfq.model_dump())
    db.add(db_rfq)
    db.commit()
    db.refresh(db_rfq)
    return db_rfq


@app.get("/rfqs", response_model=List[schemas.RFQOut])
def list_rfqs(db: Session = Depends(get_db)):
    return db.query(models.RFQ).order_by(models.RFQ.id.desc()).all()


@app.get("/rfqs/{rfq_id}", response_model=schemas.RFQOut)
def get_rfq(rfq_id: int, db: Session = Depends(get_db)):
    rfq = db.query(models.RFQ).get(rfq_id)
    if not rfq:
        raise HTTPException(404, "RFQ not found")
    return rfq


@app.post("/rfqs/{rfq_id}/quotes", response_model=schemas.QuoteOut)
def add_quote(rfq_id: int, quote: schemas.QuoteCreate, db: Session = Depends(get_db)):
    rfq = db.query(models.RFQ).get(rfq_id)
    if not rfq:
        raise HTTPException(404, "RFQ not found")
    db_quote = models.Quote(rfq_id=rfq_id, **quote.model_dump())
    db.add(db_quote)
    db.commit()
    db.refresh(db_quote)
    return db_quote


@app.get("/rfqs/{rfq_id}/quotes", response_model=List[schemas.QuoteOut])
def list_quotes(rfq_id: int, db: Session = Depends(get_db)):
    return db.query(models.Quote).filter(models.Quote.rfq_id == rfq_id).all()


@app.get("/rfqs/{rfq_id}/comparison", response_model=schemas.ComparisonResult)
def compare_quotes(rfq_id: int, db: Session = Depends(get_db)):
    rfq = db.query(models.RFQ).get(rfq_id)
    if not rfq:
        raise HTTPException(404, "RFQ not found")
    quotes = db.query(models.Quote).filter(models.Quote.rfq_id == rfq_id).all()
    ranked = rank_quotes(rfq, quotes)
    return {"rfq": rfq, "ranked_quotes": ranked}
