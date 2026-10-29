"""Code (line) coverage test cases for car_insurance_premium.

Name: Dhanush S   SRN: PES1UG24AM360   Section: F
Goal: execute every line of car_insurance_premium.py at least once.

Run:
    python -m coverage run -m pytest CodeCoverageTest_PES1UG24AM360_car_insurance_premium.py
    python -m coverage report -m
"""
import pytest

from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ----------------------------- annual_premium -----------------------------

def test_unknown_car_type_raises():
    """Line 6: the guard for a car type that is not in BASE_PREMIUM."""
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young_raises():
    """Line 8: the guard for a driver under 18."""
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_sedan_no_claims():
    """Base case: sedan 12000, zero-claim discount of 20% -> 9600."""
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_young_driver_surcharge():
    """Line 11: under 25 adds 4000. 8000 + 4000 = 12000, -20% -> 9600."""
    assert annual_premium("hatchback", 20, 0, False) == 9600


def test_senior_driver_surcharge():
    """Line 13: 60 or over adds 2000. 12000 + 2000 = 14000, -20% -> 11200."""
    assert annual_premium("sedan", 65, 0, False) == 11200


def test_many_claims_doubles_premium():
    """Line 17: more than 2 claims doubles the premium. 15000 * 2 = 30000."""
    assert annual_premium("suv", 30, 3, False) == 30000


def test_anti_theft_discount():
    """Line 19: anti-theft takes off 500. 9600 - 500 = 9100."""
    assert annual_premium("sedan", 30, 0, True) == 9100


# ----------------------------- no_claim_bonus -----------------------------

def test_negative_years_raises():
    """Line 25: negative claim-free years is invalid."""
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


def test_bonus_five_years():
    """Line 27: 5 or more claim-free years gives 50."""
    assert no_claim_bonus(5) == 50


def test_bonus_three_years():
    """Line 29: 3 or 4 claim-free years gives 35."""
    assert no_claim_bonus(3) == 35


def test_bonus_one_year():
    """Line 31: 1 or 2 claim-free years gives 20."""
    assert no_claim_bonus(1) == 20


def test_no_bonus():
    """Line 32: no claim-free years gives 0."""
    assert no_claim_bonus(0) == 0


# ------------------------------ claim_payout ------------------------------

def test_negative_damage_raises():
    """Line 37: a negative damage cost is invalid."""
    with pytest.raises(ValueError):
        claim_payout(-1, 400000, 5000, False)


def test_total_loss_pays_insured_value():
    """Line 39: a total loss pays out the full insured value."""
    assert claim_payout(50000, 400000, 5000, True) == 400000


def test_damage_below_deductible_pays_nothing():
    """Line 41: damage at or under the deductible pays nothing."""
    assert claim_payout(3000, 400000, 5000, False) == 0


def test_normal_payout_minus_deductible():
    """Lines 42 and 45: 25000 - 5000 = 20000."""
    assert claim_payout(25000, 400000, 5000, False) == 20000


def test_payout_capped_at_insured_value():
    """Line 44: a payout above the insured value is capped."""
    assert claim_payout(500000, 400000, 5000, False) == 400000
