"""
Deterministic quote-scoring engine.

Deliberately NOT an LLM call: procurement decisions need to be explainable
and reproducible, so the scoring logic here is plain, testable Python.
It's written as a single pure function (rfq, quotes) -> ranked results,
so it could later be wrapped as a callable "tool" inside an agent
orchestration layer without changing the underlying logic.
"""
from .models import RFQ, Quote

PRICE_WEIGHT = 40
LEAD_TIME_WEIGHT = 30
COMPLIANCE_WEIGHT = 30


def score_quote(rfq: RFQ, quote: Quote) -> dict:
    flags = []

    # --- Price score (lower price vs target = higher score) ---
    price_ratio = quote.price_per_unit / rfq.target_price_per_unit
    if price_ratio <= 1:
        # at or under budget: full marks, small bonus tapering as it drops further under target
        price_score = PRICE_WEIGHT
    else:
        # over budget: linearly penalize, floor at 0 once 50% over target
        overage = min(price_ratio - 1, 0.5) / 0.5
        price_score = PRICE_WEIGHT * (1 - overage)
        flags.append(
            f"Price {quote.price_per_unit:.2f}/unit is {(price_ratio - 1) * 100:.0f}% over target"
        )

    # --- Lead time score (must fit within deadline) ---
    if quote.lead_time_days <= rfq.deadline_days:
        margin = (rfq.deadline_days - quote.lead_time_days) / rfq.deadline_days
        lead_time_score = LEAD_TIME_WEIGHT * (0.7 + 0.3 * margin)  # 70-100% of weight
    else:
        lead_time_score = 0
        flags.append(
            f"Lead time {quote.lead_time_days}d exceeds deadline of {rfq.deadline_days}d"
        )

    # --- Compliance score: MOQ fit + payment terms match ---
    compliance_score = 0
    if quote.min_order_quantity <= rfq.quantity_needed:
        compliance_score += COMPLIANCE_WEIGHT * 0.5
    else:
        flags.append(
            f"MOQ {quote.min_order_quantity} exceeds requested quantity {rfq.quantity_needed}"
        )

    if quote.payment_terms.strip().lower() == rfq.preferred_payment_terms.strip().lower():
        compliance_score += COMPLIANCE_WEIGHT * 0.5
    else:
        flags.append(
            f"Payment terms '{quote.payment_terms}' differ from preferred '{rfq.preferred_payment_terms}'"
        )

    total = round(price_score + lead_time_score + compliance_score, 1)

    return {
        "quote": quote,
        "total_score": total,
        "price_score": round(price_score, 1),
        "lead_time_score": round(lead_time_score, 1),
        "compliance_score": round(compliance_score, 1),
        "flags": flags,
    }


def rank_quotes(rfq: RFQ, quotes: list[Quote]) -> list[dict]:
    scored = [score_quote(rfq, q) for q in quotes]
    return sorted(scored, key=lambda s: s["total_score"], reverse=True)
