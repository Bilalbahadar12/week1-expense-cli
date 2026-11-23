"""Functions for managing and analyzing expenses."""

from src.validators import (
    validate_amount,
    validate_category,
    validate_date,
)

SAFE_LIMIT = 0.80
EXCEEDED_LIMIT = 1.00

def add_expense(expenses, date, category, amount, description):
    """Add a new expense to the expense list."""

    expense = {
        "id":len(expenses) + 1,
        "date": date,
        "category":category,
        "amount":amount,
        "description":description
    }

    expenses.append(expense)

    return expense


# expenses = []
# print(add_expense(expenses, '2026-11-20', 'Food', 500, 'Lunch'))

# print(expenses)




def filter_by_category(expenses, category):
    """Return expenses matching the selected category."""

    filtered_expenses = []

    for expense in expenses:
        if expense["category"] == category:
            filtered_expenses.append(expense)

    return filtered_expenses

def filter_by_date_range(expenses, start, end):
    """Return expenses with start <= date <= end (inclusive)."""
    start, end = validate_date(start), validate_date(end)
    if start > end:
        raise ValueError("Start date must not be after end date.")
    return [e for e in expenses if start <= e["date"] <= end]


def get_category_totals(expenses):
    """Calculate total spending for each category."""

    category_totals ={}

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals


# expenses = []
# add_expense(expenses, '2026-11-20', 'Food', 500, 'Lunch')
# add_expense(expenses, '2026-11-20', 'Transport', 200, 'Bus')
# add_expense(expenses, '2026-11-20', 'Food', 300, 'Dinner')
# add_expense(expenses, '2026-11-20', 'Entertainment', 400, 'Movie')
# print(get_category_totals(expenses))

def get_category_percentages(expenses):
    """Return {category: percentage share of total spend}."""
    totals = get_category_totals(expenses)
    grand_total = sum(totals.values())
    if grand_total == 0:
        return {}
    return {c: t / grand_total * 100 for c, t in totals.items()}



def check_budget_status(spent, budgets, category, month):
    """Check monthly spending against a category budget."""

    if category not in budgets:
        return {
            "spent": 0,
            "budget": 0,
            "percentage": 0,
            "status": "No Budget Set"
        }

    total_spent = 0

    for expense in spent:
        if (
            expense["category"] == category
            and expense["date"][:7] == month
        ):
            total_spent += expense["amount"]

    budget = budgets[category]

    if budget <= 0:
        raise ValueError("Budget must be greater than zero.")

    percentage = (total_spent / budget) * 100

    if percentage < 80:
        status = "Safe"
    elif percentage <= 100:
        status = "Warning"
    else:
        status = "Exceeded"

    return {
        "spent": total_spent,
        "budget": budget,
        "percentage": percentage,
        "status": status
    }



def compute_summary_tuple(expenses):
    """Calculate summary metrics and return them as a tuple."""

    if not expenses:
        return (0, 0, 0, 0)

    amounts = [expense["amount"] for expense in expenses]

    total_spend = sum(amounts)
    average_spend = total_spend / len(amounts)
    highest_expense = max(amounts)
    lowest_expense = min(amounts)

    return (
        total_spend,
        average_spend,
        highest_expense,
        lowest_expense
    )

