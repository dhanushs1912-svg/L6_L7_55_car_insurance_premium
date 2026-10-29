"""Branch coverage test cases for car_insurance_premium.

Name: Dhanush S   SRN: PES1UG24AM360   Section: F

Line coverage only asks whether a line ran. Branch coverage asks whether every
decision went BOTH ways. This file keeps the line-coverage cases and adds the
False side of every decision that the line-coverage file never exercised.

Run:
    python -m coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM360_car_insurance_premium.py
    python -m coverage report -m
"""
import pytest

from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout


# ----------------------------- annual_premium -----------------------------

def test_unknown_car_type_raises():
    """car_type guard: True side."""
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_known_car_type_passes_guard():
    """car_type guard: False side."""
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_driver_too_young_raises():
    """age guard: True side."""
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_adult_driver_passes_guard():
    """age guard: False side, exactly on the boundary of 18."""
    assert annual_premium("hatchback", 18, 0, False) == 9600


def test_young_driver_surcharge():
    """age < 25: True side. 8000 + 4000 = 12000, -20% -> 9600."""
    assert annual_premium("hatchback", 20, 0, False) == 9600


def test_senior_driver_surcharge():
    """age < 25 False, age >= 60 True. 12000 + 2000 = 14000, -20% -> 11200."""
    assert annual_premium("sedan", 65, 0, False) == 11200


def test_middle_aged_driver_no_surcharge():
    """Both age branches False: no surcharge is applied."""
    assert annual_premium("suv", 40, 0, False) == 12000


def test_zero_claims_discount():
    """claims == 0: True side."""
    assert annual_premium("suv", 40, 0, False) == 12000


def test_many_claims_doubles_premium():
    """claims == 0 False, claims > 2 True. 15000 * 2 = 30000."""
    assert annual_premium("suv", 30, 3, False) == 30000


def test_moderate_claims_no_adjustment():
    """BOTH claim branches False - the branch the line tests never reach.

    One or two claims means neither the discount nor the doubling applies,
    so the premium stays at base plus any age surcharge.
    15000 + 2000 (age 65) = 17000, then -500 for anti-theft = 16500.
    """
    assert annual_premium("suv", 65, 1, True) == 16500


def test_two_claims_no_adjustment():
    """The upper edge of the same untaken branch: 2 claims changes nothing."""
    assert annual_premium("sedan", 30, 2, False) == 12000


def test_anti_theft_discount():
    """anti-theft: True side. 9600 - 500 = 9100."""
    assert annual_premium("sedan", 30, 0, True) == 9100


def test_without_anti_theft():
    """anti-theft: False side."""
    assert annual_premium("sedan", 30, 0, False) == 9600


# ----------------------------- no_claim_bonus -----------------------------

def test_negative_years_raises():
    """years < 0: True side."""
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


def test_bonus_five_years():
    """years >= 5: True side."""
    assert no_claim_bonus(5) == 50


def test_bonus_four_years():
    """years >= 5 False, years >= 3 True."""
    assert no_claim_bonus(4) == 35


def test_bonus_three_years():
    """Boundary of the 35 band."""
    assert no_claim_bonus(3) == 35


def test_bonus_two_years():
    """years >= 3 False, years >= 1 True."""
    assert no_claim_bonus(2) == 20


def test_bonus_one_year():
    """Boundary of the 20 band."""
    assert no_claim_bonus(1) == 20


def test_no_bonus():
    """Every band False: falls through to 0."""
    assert no_claim_bonus(0) == 0


# ------------------------------ claim_payout ------------------------------

def test_negative_damage_raises():
    """Amount guard: True via the first condition."""
    with pytest.raises(ValueError):
        claim_payout(-1, 400000, 5000, False)


def test_negative_deductible_raises():
    """Amount guard: True via the second condition of the or."""
    with pytest.raises(ValueError):
        claim_payout(25000, 400000, -5000, False)


def test_valid_amounts_pass_guard():
    """Amount guard: False side."""
    assert claim_payout(25000, 400000, 5000, False) == 20000


def test_total_loss_pays_insured_value():
    """is_total_loss: True side."""
    assert claim_payout(50000, 400000, 5000, True) == 400000


def test_not_total_loss_continues():
    """is_total_loss: False side."""
    assert claim_payout(25000, 400000, 5000, False) == 20000


def test_damage_below_deductible_pays_nothing():
    """damage <= deductible: True side."""
    assert claim_payout(3000, 400000, 5000, False) == 0


def test_damage_equal_to_deductible_pays_nothing():
    """The boundary of the same decision."""
    assert claim_payout(5000, 400000, 5000, False) == 0


def test_normal_payout_minus_deductible():
    """damage <= deductible False: 25000 - 5000 = 20000."""
    assert claim_payout(25000, 400000, 5000, False) == 20000


def test_payout_capped_at_insured_value():
    """payout > insured_value: True side."""
    assert claim_payout(500000, 400000, 5000, False) == 400000


def test_payout_within_insured_value():
    """payout > insured_value: False side."""
    assert claim_payout(25000, 400000, 5000, False) == 20000
