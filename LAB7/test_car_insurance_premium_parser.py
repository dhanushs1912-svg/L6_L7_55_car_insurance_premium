"""Hypothesis fuzz tests for car_insurance_premium_parser.

Name: Dhanush S   SRN: PES1UG24AM360   Section: F

Each test states one property: the function must not crash, whatever it is
given. Hypothesis generates hundreds of inputs per run - random text, empty
strings and None - and shrinks any failure down to the smallest input that
still breaks the function.

Run:
    python -m pytest test_car_insurance_premium_parser.py
"""
from hypothesis import given, strategies as st

from car_insurance_premium_parser import (
    normalize_registration,
    total_claim_amount,
    driver_age,
)


@given(st.text() | st.none())
def test_normalize_registration_no_crash(s):
    """normalize_registration must handle any text or None without crashing."""
    try:
        normalize_registration(s)
    except Exception as exc:
        assert False, (
            f"normalize_registration crashed on {s!r} "
            f"with {type(exc).__name__}: {exc}"
        )


@given(st.text() | st.none())
def test_total_claim_amount_no_crash(s):
    """total_claim_amount must handle any text or None without crashing."""
    try:
        total_claim_amount(s)
    except Exception as exc:
        assert False, (
            f"total_claim_amount crashed on {s!r} "
            f"with {type(exc).__name__}: {exc}"
        )


@given(st.text() | st.none())
def test_driver_age_no_crash(s):
    """driver_age must handle any text or None without crashing."""
    try:
        driver_age(s)
    except Exception as exc:
        assert False, (
            f"driver_age crashed on {s!r} "
            f"with {type(exc).__name__}: {exc}"
        )
