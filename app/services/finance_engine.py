"""Deterministic finance maths. Inga AI use pannala, ella calculation-um exact Decimal-la."""
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal('0.01')
ZERO = Decimal('0')


def money(value):
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)


def to_annual(amount, frequency):
    amount = Decimal(amount)
    return amount * 12 if frequency == 'monthly' else amount


def to_monthly(amount, frequency):
    return money(to_annual(amount, frequency) / 12)


def summarize_budget(incomes, expenses):
    """incomes: Income rows, expenses: oru month-oda Expense rows."""
    annual_income = sum((to_annual(i.amount, i.frequency) for i in incomes), ZERO)
    monthly_income = money(annual_income / 12)
    total_expenses = money(sum((Decimal(e.amount) for e in expenses), ZERO))
    remaining = money(monthly_income - total_expenses)

    if monthly_income > 0:
        savings_rate = money(remaining / monthly_income * 100)
    else:
        savings_rate = money(0)

    by_category = {}
    for e in expenses:
        by_category[e.category] = by_category.get(e.category, ZERO) + Decimal(e.amount)
    by_category = {k: money(v) for k, v in by_category.items()}

    return {
        'annual_income': money(annual_income),
        'monthly_income': monthly_income,
        'total_expenses': total_expenses,
        'remaining': remaining,
        'savings_rate': savings_rate,
        'by_category': by_category,
    }