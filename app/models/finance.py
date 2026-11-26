from datetime import datetime, timezone
from ..extensions import db

EXPENSE_CATEGORIES = [
    ('rent', 'Rent'),
    ('food', 'Food'),
    ('transport', 'Transportation'),
    ('utilities', 'Electricity & Utilities'),
    ('education', 'Education'),
    ('emi', 'EMI & Loans'),
    ('family', 'Family'),
    ('other', 'Other'),
]

INCOME_FREQUENCIES = [
    ('monthly', 'Monthly'),
    ('annual', 'Annual'),
]


class Income(db.Model):
    __tablename__ = 'income'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    source = db.Column(db.String(60), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    frequency = db.Column(db.String(10), nullable=False, default='monthly')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    category = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    month = db.Column(db.Date, nullable=False, index=True)  # month-oda 1st date
    note = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))