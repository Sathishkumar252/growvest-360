from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, NumberRange

AMOUNT_MAX = Decimal('100000000')
COMPOUNDING = [(1, 'Yearly'), (2, 'Half-yearly'), (4, 'Quarterly'), (12, 'Monthly')]


def amount_field(label, default):
    return DecimalField(
        label, places=2, default=Decimal(default),
        validators=[InputRequired(), NumberRange(min=Decimal('1'), max=AMOUNT_MAX)])


def rate_field(label, default, note):
    return DecimalField(
        label, places=2, default=Decimal(default), description=note,
        validators=[InputRequired(), NumberRange(min=Decimal('0'), max=Decimal('50'))])


def years_field(label, default):
    return IntegerField(
        label, default=default,
        validators=[InputRequired(), NumberRange(min=1, max=50)])


def months_field(label, default):
    return IntegerField(
        label, default=default,
        validators=[InputRequired(), NumberRange(min=1, max=240)])


def compounding_field(default):
    return SelectField('Compounding', choices=COMPOUNDING, coerce=int, default=default)


class SIPForm(FlaskForm):
    monthly_amount = amount_field('Monthly investment (INR)', '5000')
    annual_return = rate_field(
        'Expected annual return (%)', '12',
        'Assumed, not guaranteed. Market-linked returns can be lower or even negative.')
    years = years_field('Investment period (years)', 10)
    submit = SubmitField('Calculate')


class FDForm(FlaskForm):
    principal = amount_field('Deposit amount (INR)', '100000')
    annual_rate = rate_field(
        'Interest rate (% per year)', '7',
        'Enter the rate your bank offers. Bank rates change, so please check with your bank.')
    months = months_field('Tenure (months)', 12)
    compounding = compounding_field(4)
    submit = SubmitField('Calculate')


class RDForm(FlaskForm):
    monthly_amount = amount_field('Monthly deposit (INR)', '5000')
    annual_rate = rate_field(
        'Interest rate (% per year)', '6.5',
        'Enter the rate your bank offers. Bank rates change, so please check with your bank.')
    months = months_field('Tenure (months)', 12)
    compounding = compounding_field(4)
    submit = SubmitField('Calculate')


class CompoundForm(FlaskForm):
    principal = amount_field('Principal (INR)', '100000')
    annual_rate = rate_field('Annual rate (%)', '8', 'The rate you want to test. It is an assumption, not a promise.')
    years = years_field('Time period (years)', 10)
    compounding = compounding_field(1)
    submit = SubmitField('Calculate')