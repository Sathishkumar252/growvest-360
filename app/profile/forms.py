from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import Optional, InputRequired, Length, NumberRange


class ProfileForm(FlaskForm):
    full_name = StringField('Full name', validators=[Optional(), Length(max=80)])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=18, max=100)])
    family_members = IntegerField(
        'Family members you support (including you)',
        default=1,
        validators=[InputRequired(), NumberRange(min=1, max=20)])
    risk_tolerance = SelectField(
        'Risk tolerance',
        choices=[
            ('low', 'Low - I prefer safety'),
            ('medium', 'Medium - balanced'),
            ('high', 'High - I can accept ups and downs'),
        ],
        default='medium',
        description='Used only to explain which options may suit your comfort level. Not financial advice.')
    horizon_years = IntegerField(
        'Investment horizon (years)',
        default=5,
        validators=[InputRequired(), NumberRange(min=1, max=40)])
    emergency_target_months = IntegerField(
        'Emergency fund target (months of expenses)',
        default=6,
        validators=[InputRequired(), NumberRange(min=1, max=24)],
        description='Many planners suggest keeping 3 to 6 months of expenses as an emergency fund.')
    submit = SubmitField('Save Profile')