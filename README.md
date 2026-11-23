# Personal Expense & Budget CLI Analyzer

IT Simplera – Week 1, Task 1 (Python Development).
A menu-driven CLI that records expenses, filters them, enforces monthly
category budgets and prints analytics. Pure Python standard library; pytest is
used only for tests.

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python -m src.main
```

## Test
```bash
python -m pytest -v
```

## Features
1. Add expense (date `YYYY-MM-DD`, category, positive amount, description)
2. View all expenses in an aligned table
3. Filter by category
4. Set monthly budget per category
5. Analytics report: total, average, highest, lowest, % share per category,
   and budget status (Safe < 80%, Warning 80–100%, Exceeded > 100%)
6. Exit

## Project structure
```
src/main.py        CLI menu and routing
src/analytics.py   storage helpers, budget checks, summary metrics
src/validators.py  date / amount / category validation
tests/             assert-based tests
```


