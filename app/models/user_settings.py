from ..extensions import db


class UserSettings(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    family_members = db.Column(db.Integer, nullable=False, default=1)
    risk_tolerance = db.Column(db.String(10), nullable=False, default='medium')
    horizon_years = db.Column(db.Integer, nullable=False, default=5)
    emergency_target_months = db.Column(db.Integer, nullable=False, default=6)

    user = db.relationship(
        'User',
        backref=db.backref('settings', uselist=False, cascade='all, delete-orphan'),
    )