"""Interactive CLI menu for the Personal Expense & Budget Analyzer.

Run from the project root:  python -m src.main
"""
from src import analytics

from src.validators import (
    VALID_CATEGORIES,
    validate_amount,
    validate_category,
)

MENU = """
=== Expense & Budget Analyzer ===
1. Add Expense
2. View All
3. Filter by Category
4. Set Budget
5. Analytics Report
6. Exit
"""


def prompt_until_valid(label, validator):
    """Keep asking for input until ``validator`` accepts it."""
    while True:
        value = input(label).strip()
        try:
            return validator(value)
        except ValueError as err:
            print(f"  ! {err}")


def print_table(expenses):
    """Print expenses as an aligned table."""
    if not expenses:
        print("No expenses to show.")
        return
    header = f"{'ID':<4}{'Date':<12}{'Category':<15}{'Amount':>12}  Description"
    print(header)
    print("-" * len(header))
    for e in expenses:
        print(
            f"{e['id']:<4}{e['date']:<12}{e['category']:<15}"
            f"{e['amount']:>12,.2f}  {e['description']}"
        )


def handle_add(expenses):
    """Menu option 1."""
    date = prompt_until_valid("Date (YYYY-MM-DD): ", analytics.validate_date)
    category = prompt_until_valid(
        f"Category ({', '.join(sorted(VALID_CATEGORIES))}): ", validate_category
    )
    amount = prompt_until_valid("Amount: ", validate_amount)
    description = input("Description: ")
    record = analytics.add_expense(expenses, date, category, amount, description)
    print(f"Added expense #{record['id']}.")


def handle_filter(expenses):
    """Menu option 3."""
    category = prompt_until_valid("Category: ", validate_category)
    print_table(analytics.filter_by_category(expenses, category))


def handle_budget(budgets):
    """Menu option 4."""
    category = prompt_until_valid("Category: ", validate_category)
    budgets[category] = prompt_until_valid("Monthly budget: ", validate_amount)
    print(f"Budget for {category} set to {budgets[category]:,.2f}.")


def handle_report(expenses, budgets):
    """Menu option 5."""
    if not expenses:
        print("No expenses recorded yet.")
        return
    total, average, highest, lowest = analytics.compute_summary_tuple(expenses)
    print(f"\nTotal spend : {total:,.2f}")
    print(f"Average     : {average:,.2f}")
    print(f"Highest     : {highest:,.2f}")
    print(f"Lowest      : {lowest:,.2f}\n")

    month = max(e["date"] for e in expenses)[:7]
    month_totals = analytics.get_category_totals(expenses)
    shares = analytics.get_category_percentages(expenses)
    print(f"{'Category':<15}{'Share':>8}{'Spent (' + month + ')':>20}{'Budget':>12}  Status")
    print("-" * 70)
    for category in sorted(VALID_CATEGORIES):
        result = analytics.check_budget_status(
            expenses, budgets, category, month
        )

        spent = result["spent"]
        budget = result["budget"]
        status = result["status"]

        budget_text = f"{budget:,.2f}" if budget is not None else "-"

        print(
            f"{category:<15}{shares.get(category, 0.0):>7.1f}%"
            f"{spent:>20,.2f}{budget_text:>12}  {status}"
        )


def main():
    """Run the menu loop."""
    expenses, budgets = [], {}
    while True:
        print(MENU)
        try:
            choice = input("Choose an option (1-6): ").strip()
            if choice == "1":
                handle_add(expenses)
            elif choice == "2":
                print_table(expenses)
            elif choice == "3":
                handle_filter(expenses)
            elif choice == "4":
                handle_budget(budgets)
            elif choice == "5":
                handle_report(expenses, budgets)
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("  ! Please enter a number from 1 to 6.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
