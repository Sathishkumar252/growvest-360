from decimal import Decimal
from flask import Blueprint, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import InputRequired, NumberRange
from ..services import investment_engine as eng
from .forms import amount_field, rate_field, years_field

advanced_bp = Blueprint('advanced', __name__, url_prefix='/calculators')


class GoldForm(FlaskForm):
    amount = amount_field('Amount to invest today (INR)', '100000')
    annual_growth = DecimalField(
        'Assumed yearly gold price growth (%)', places=2, default=Decimal('8'),
        validators=[InputRequired(), NumberRange(min=Decimal('-20'), max=Decimal('50'))],
        description='An assumption, not a forecast. Gold prices can rise or fall. You can enter a negative number to test a fall.')
    years = years_field('Holding period (years)', 10)
    submit = SubmitField('Show scenarios')


class CompareForm(FlaskForm):
    monthly_amount = amount_field('Monthly amount (INR)', '5000')
    years = years_field('Period (years)', 10)
    sip_rate = rate_field('Equity SIP: assumed return (% per year)', '12',
                          'Assumed, not guaranteed. Market returns can be lower or negative.')
    rd_rate = rate_field('RD: bank interest rate (% per year)', '6.5',
                         "Check your bank's current RD rate.")
    gold_rate = rate_field('Gold: assumed price growth (% per year)', '8',
                           'Assumed, not guaranteed.')
    savings_rate = rate_field('Savings account interest (% per year)', '3',
                              'Banks can change this rate at any time.')
    submit = SubmitField('Compare')


@advanced_bp.route('/gold', methods=['GET', 'POST'])
@login_required
def gold():
    form = GoldForm()
    scenarios = None
    if form.validate_on_submit():
        scenarios = eng.gold_scenarios(
            form.amount.data, form.annual_growth.data, form.years.data * 12)
    chart = None
    if scenarios:
        chart = {
            'labels': [s['scenario'] for s in scenarios],
            'values': [float(s['future_value']) for s in scenarios],
            'invested': float(scenarios[0]['invested']),
        }
    return render_template('calculators/gold.html', form=form, scenarios=scenarios, chart=chart)


@advanced_bp.route('/compare', methods=['GET', 'POST'])
@login_required
def compare():
    form = CompareForm()
    items = None
    chart = None
    if form.validate_on_submit():
        rates = {
            'sip': form.sip_rate.data,
            'rd': form.rd_rate.data,
            'gold': form.gold_rate.data,
            'savings': form.savings_rate.data,
        }
        years = form.years.data
        items = eng.compare_monthly(form.monthly_amount.data, years, rates)
        chart = {
            'labels': ['Year %d' % y for y in range(1, years + 1)],
            'datasets': [{'name': i['name'], 'data': i['series']} for i in items],
            'invested': [float(form.monthly_amount.data * 12 * y) for y in range(1, years + 1)],
        }
    return render_template('calculators/compare.html', form=form, items=items, chart=chart)