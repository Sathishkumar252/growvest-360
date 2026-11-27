"""Dashboard-ku venum numbers + chart data. Deterministic, AI use pannala."""
from datetime import date
from decimal import Decimal
from ..extensions import db
from ..models.finance import Income, Expense, EXPENSE_CATEGORIES
from .finance_engine import summarize_budget, money, ZERO

LABELS = dict(EXPENSE_CATEGORIES)


def last_months(end, n=6):
    """end month varaikkum last n months (1st date list)."""
    months = []
    y, m = end.year, end.month
    for _ in range(n):
        months.append(date(y, m, 1))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(months))


def assess_health(summary, settings):
    months = settings.emergency_target_months if settings else 6
    target = money(summary['total_expenses'] * months)
    income = summary['monthly_income']
    rate = summary['savings_rate']

    base = {'emergency_target': target, 'months': months}
    if income <= 0:
        return {**base, 'label': 'No data yet', 'tone': 'info',
                'message': 'Add your income in the Salary Analyzer to see your financial health overview.'}
    if summary['remaining'] < 0:
        return {**base, 'label': 'Needs attention', 'tone': 'danger',
                'message': 'Your expenses are higher than your income this month. Review your spending before thinking about investments.'}
    if rate < 10:
        return {**base, 'label': 'Tight', 'tone': 'warning',
                'message': 'You are saving less than 10% of your income. Small cuts in non-essential spending could build more room.'}
    if rate < 20:
        return {**base, 'label': 'Fair', 'tone': 'info',
                'message': 'You are saving a reasonable share of your income. Many planners use 20% as a common savings guideline (for example the 50/30/20 rule).'}
    if rate < 30:
        return {**base, 'label': 'Good', 'tone': 'success',
                'message': 'You are meeting or beating the common 20% savings guideline. Keep your emergency fund in mind before taking market risk.'}
    return {**base, 'label': 'Strong', 'tone': 'success',
            'message': 'You are saving more than 30% of your income this month. A strong base for planning goals and an emergency fund.'}


def build_dashboard(user_id, month, settings=None):
    months = last_months(month, 6)

    # Ella query-yum user_id vechu filter (data isolation)
    incomes = db.session.scalars(
        db.select(Income).where(Income.user_id == user_id)).all()
    expenses = db.session.scalars(
        db.select(Expense).where(
            Expense.user_id == user_id,
            Expense.month >= months[0],
            Expense.month <= month)).all()

    by_month = {m: [] for m in months}
    for e in expenses:
        by_month.setdefault(e.month, []).append(e)

    summary = summarize_budget(incomes, by_month.get(month, []))

    trend_expenses = [
        float(money(sum((Decimal(e.amount) for e in by_month[m]), ZERO)))
        for m in months
    ]
    trend_income = [float(summary['monthly_income'])] * len(months)

    cat_labels = [LABELS.get(k, k) for k in summary['by_category']]
    cat_values = [float(v) for v in summary['by_category'].values()]

    return {
        'summary': summary,
        'health': assess_health(summary, settings),
        'income_count': len(incomes),
        'charts': {
            'trend': {
                'labels': [m.strftime('%b %Y') for m in months],
                'income': trend_income,
                'expenses': trend_expenses,
            },
            'categories': {'labels': cat_labels, 'values': cat_values},
        },
    }