from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import DecimalField
from wtforms.validators import InputRequired, Optional, NumberRange

MAX_AMOUNT = Decimal('100000000')


def _optional_amount(label):
    return DecimalField(label, places=2,
                        validators=[Optional(), NumberRange(min=Decimal('0'), max=MAX_AMOUNT)])


class PlanForm(FlaskForm):
    saved = DecimalField(
        'Emergency fund saved so far (INR)', places=2, default=Decimal('0'),
        validators=[InputRequired(), NumberRange(min=Decimal('0'), max=MAX_AMOUNT)],
        description='Money you already keep aside only for emergencies (savings account, liquid fund or FD). Enter 0 if you have none yet.')
    custom_emergency = _optional_amount('Emergency fund (INR)')
    custom_invest = _optional_amount('Investing (INR)')
    custom_buffer = _optional_amount('Wants and flexibility (INR)')