"""Shared validation and exact decimal rounding for DPCL edit budgets."""

from fractions import Fraction


def validate_edit_budget(bottom_k, bottom_k_percent):
    if bottom_k is not None and bottom_k_percent is not None:
        raise ValueError("bottom_k and bottom_k_percent are mutually exclusive")
    if bottom_k is not None and (type(bottom_k) is not int or bottom_k < 0):
        raise ValueError("bottom_k must be a nonnegative integer")
    if bottom_k_percent is not None and (
            type(bottom_k_percent) not in (int, float) or not 0 <= bottom_k_percent <= 100):
        raise ValueError("bottom_k_percent must be a finite percentage in [0, 100]")


def percent_caps(batch_slots, percent):
    """Ceiling of the decimal percentage for each possible valid batch size."""
    ratio = Fraction(str(percent)) / 100
    numerator, denominator = ratio.numerator, ratio.denominator
    return [(n * numerator + denominator - 1) // denominator for n in range(batch_slots + 1)]
