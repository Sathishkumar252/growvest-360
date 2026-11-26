from datetime import date, datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models.finance import Income, Expense, EXPENSE_CATEGORIES
from ..services.finance_engine import summarize_budget, to_monthly
from .forms import IncomeForm, ExpenseForm

salary_bp = Blueprint('salary', __name__, url_prefix='/salary')
CATEGORY_LABELS = dict(EXPENSE_CATEGORIES)


def month_arg():
    """?month=2026-11 maathiri value-ah date-ah maathum. Thappaa irundha ippodhaiya month."""
    value = request.values.get('month')
    try:
        return datetime.strptime(value, '%Y-%m').date().replace(day=1)
    except (TypeError, ValueError):
        return date.today().replace(day=1)


def render_page(income_form, expense_form, month):
    # Ella query-yum current_user.id vechu filter (data isolation)
    incomes = db.session.scalars(
        db.select(Income).filter_by(user_id=current_user.id).order_by(Income.id)).all()
    expenses = db.session.scalars(
        db.select(Expense).filter_by(user_id=current_user.id, month=month)
        .order_by(Expense.id.desc())).all()
    return render_template(
        'salary/index.html',
        income_form=income_form, expense_form=expense_form,
        incomes=incomes, expenses=expenses,
        summary=summarize_budget(incomes, expenses),
        month_value=month.strftime('%Y-%m'),
        month_label=month.strftime('%B %Y'),
        labels=CATEGORY_LABELS,
        to_monthly=to_monthly,
    )


@salary_bp.route('/')
@login_required
def index():
    return render_page(IncomeForm(), ExpenseForm(), month_arg())


@salary_bp.route('/income/add', methods=['POST'])
@login_required
def add_income():
    month = month_arg()
    form = IncomeForm()
    if form.validate_on_submit():
        db.session.add(Income(
            user_id=current_user.id,
            source=form.source.data.strip(),
            amount=form.income_amount.data,
            frequency=form.frequency.data,
        ))
        db.session.commit()
        flash('Income added.', 'success')
        return redirect(url_for('salary.index', month=month.strftime('%Y-%m')))
    return render_page(form, ExpenseForm(), month)


@salary_bp.route('/expense/add', methods=['POST'])
@login_required
def add_expense():
    month = month_arg()
    form = ExpenseForm()
    if form.validate_on_submit():
        db.session.add(Expense(
            user_id=current_user.id,
            category=form.category.data,
            amount=form.expense_amount.data,
            month=month,
            note=(form.note.data or '').strip() or None,
        ))
        db.session.commit()
        flash('Expense added.', 'success')
        return redirect(url_for('salary.index', month=month.strftime('%Y-%m')))
    return render_page(IncomeForm(), form, month)


@salary_bp.route('/income/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_income(item_id):
    item = db.session.scalar(db.select(Income).filter_by(id=item_id, user_id=current_user.id))
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash('Income deleted.', 'info')
    return redirect(url_for('salary.index', month=month_arg().strftime('%Y-%m')))


@salary_bp.route('/expense/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_expense(item_id):
    item = db.session.scalar(db.select(Expense).filter_by(id=item_id, user_id=current_user.id))
    if item is None:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash('Expense deleted.', 'info')
    return redirect(url_for('salary.index', month=month_arg().strftime('%Y-%m')))