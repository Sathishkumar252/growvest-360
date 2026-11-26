from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Optional
from ..models.finance import EXPENSE_CATEGORIES, INCOME_FREQUENCIES

MAX_AMOUNT = Decimal('100000000')
MIN_AMOUNT = Decimal('0.01')


class IncomeForm(FlaskForm):
    source = StringField('Income source', validators=[DataRequired(), Length(max=60)],
                         render_kw={'placeholder': 'e.g. Salary'})
    income_amount = DecimalField('Amount (INR)', places=2,
                                 validators=[InputRequired(), NumberRange(min=MIN_AMOUNT, max=MAX_AMOUNT)])
    frequency = SelectField('Frequency', choices=INCOME_FREQUENCIES, default='monthly')
    submit = SubmitField('Add Income')


class ExpenseForm(FlaskForm):
    category = SelectField('Category', choices=EXPENSE_CATEGORIES)
    expense_amount = DecimalField('Amount (INR)', places=2,
                                  validators=[InputRequired(), NumberRange(min=MIN_AMOUNT, max=MAX_AMOUNT)])
    note = StringField('Note (optional)', validators=[Optional(), Length(max=120)])
    submit = SubmitField('Add Expense')