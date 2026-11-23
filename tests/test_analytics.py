"""Input validation helpers for the Expense & Budget CLI Analyzer."""

import math
from datetime import datetime

VALID_CATEGORIES = {"Food", "Transport", "Utilities", "Entertainment", "Other"}


def validate_amount(val):
    """Return ``val`` as a float if it is a finite number greater than 0.

    Raises:
        ValueError: if the value is not numeric, not finite, or not positive.
    """
    try:
        amount = float(str(val).replace(",", "").strip())
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.") from None
    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
    return amount


def validate_date(date_str):
    """Validate a date string in strict YYYY-MM-DD format.

    Raises:
        ValueError: if the string is not a real, zero-padded date.
    """
    error = ValueError("Invalid date. Use YYYY-MM-DD format.")
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise error from None
    # Reject non-padded forms such as "2026-1-5" that strptime accepts.
    if parsed.strftime("%Y-%m-%d") != date_str:
        raise error
    return date_str


def validate_category(cat):
    """Return the canonical category name (case-insensitive match).

    Raises:
        ValueError: if the category is not in VALID_CATEGORIES.
    """
    if isinstance(cat, str):
        cleaned = cat.strip().title()
        if cleaned in VALID_CATEGORIES:
            return cleaned
    options = ", ".join(sorted(VALID_CATEGORIES))
    raise ValueError(f"Invalid category. Choose one of: {options}.")
