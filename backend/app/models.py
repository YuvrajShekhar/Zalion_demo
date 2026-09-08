from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    quantity_needed = Column(Integer, nullable=False)
    target_price_per_unit = Column(Float, nullable=False)
    deadline_days = Column(Integer, nullable=False)  # max acceptable lead time
    preferred_payment_terms = Column(String, nullable=False)  # e.g. "Net 30"
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    quotes = relationship("Quote", back_populates="rfq", cascade="all, delete-orphan")


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"), nullable=False)
    supplier_name = Column(String, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    lead_time_days = Column(Integer, nullable=False)
    min_order_quantity = Column(Integer, nullable=False)
    payment_terms = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    rfq = relationship("RFQ", back_populates="quotes")
