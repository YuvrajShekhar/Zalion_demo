import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models import RFQ, Quote
from app.scoring import score_quote, rank_quotes


def make_rfq(**overrides):
    defaults = dict(
        id=1,
        title="Test RFQ",
        quantity_needed=1000,
        target_price_per_unit=2.5,
        deadline_days=21,
        preferred_payment_terms="Net 30",
    )
    defaults.update(overrides)
    return RFQ(**defaults)


def make_quote(**overrides):
    defaults = dict(
        id=1,
        rfq_id=1,
        supplier_name="Test Supplier",
        price_per_unit=2.3,
        lead_time_days=18,
        min_order_quantity=500,
        payment_terms="Net 30",
    )
    defaults.update(overrides)
    return Quote(**defaults)


def test_quote_at_or_under_budget_gets_full_price_score():
    rfq = make_rfq()
    quote = make_quote(price_per_unit=2.0)
    result = score_quote(rfq, quote)
    assert result["price_score"] == 40.0
    assert not any("Price" in f for f in result["flags"])


def test_quote_over_budget_is_penalized_and_flagged():
    rfq = make_rfq()
    quote = make_quote(price_per_unit=3.0)  # 20% over target
    result = score_quote(rfq, quote)
    assert result["price_score"] < 40.0
    assert any("Price" in f for f in result["flags"])


def test_lead_time_within_deadline_scores_positively():
    rfq = make_rfq(deadline_days=21)
    quote = make_quote(lead_time_days=10)
    result = score_quote(rfq, quote)
    assert result["lead_time_score"] > 0
    assert not any("Lead time" in f for f in result["flags"])


def test_lead_time_over_deadline_scores_zero_and_flags():
    rfq = make_rfq(deadline_days=14)
    quote = make_quote(lead_time_days=20)
    result = score_quote(rfq, quote)
    assert result["lead_time_score"] == 0
    assert any("Lead time" in f for f in result["flags"])


def test_moq_over_requested_quantity_flags():
    rfq = make_rfq(quantity_needed=1000)
    quote = make_quote(min_order_quantity=2000)
    result = score_quote(rfq, quote)
    assert any("MOQ" in f for f in result["flags"])
    assert result["compliance_score"] == 15.0  # only payment-terms half awarded


def test_payment_terms_mismatch_flags():
    rfq = make_rfq(preferred_payment_terms="Net 30")
    quote = make_quote(payment_terms="Net 60")
    result = score_quote(rfq, quote)
    assert any("Payment terms" in f for f in result["flags"])


def test_fully_compliant_quote_has_no_flags():
    rfq = make_rfq()
    quote = make_quote(price_per_unit=2.0, lead_time_days=10, min_order_quantity=100, payment_terms="Net 30")
    result = score_quote(rfq, quote)
    assert result["flags"] == []


def test_rank_quotes_sorts_descending_by_total_score():
    rfq = make_rfq()
    good = make_quote(id=1, price_per_unit=2.0, lead_time_days=10)
    bad = make_quote(id=2, price_per_unit=4.0, lead_time_days=30, min_order_quantity=5000, payment_terms="Net 90")
    ranked = rank_quotes(rfq, [bad, good])
    assert ranked[0]["quote"].id == 1
    assert ranked[0]["total_score"] > ranked[1]["total_score"]
