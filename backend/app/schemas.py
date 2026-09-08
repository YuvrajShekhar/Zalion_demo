from pydantic import BaseModel, Field
from typing import List


class RFQCreate(BaseModel):
    title: str
    quantity_needed: int = Field(gt=0)
    target_price_per_unit: float = Field(gt=0)
    deadline_days: int = Field(gt=0)
    preferred_payment_terms: str


class RFQOut(RFQCreate):
    id: int

    class Config:
        from_attributes = True


class QuoteCreate(BaseModel):
    supplier_name: str
    price_per_unit: float = Field(gt=0)
    lead_time_days: int = Field(gt=0)
    min_order_quantity: int = Field(gt=0)
    payment_terms: str


class QuoteOut(QuoteCreate):
    id: int
    rfq_id: int

    class Config:
        from_attributes = True


class ScoredQuote(BaseModel):
    quote: QuoteOut
    total_score: float
    price_score: float
    lead_time_score: float
    compliance_score: float
    flags: List[str]


class ComparisonResult(BaseModel):
    rfq: RFQOut
    ranked_quotes: List[ScoredQuote]
