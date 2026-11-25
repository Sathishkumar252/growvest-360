from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from ..extensions import db
from ..models.user import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=30),
        Regexp(r'^[A-Za-z0-9_]+$', message='Letters, numbers and underscore only.')])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        if db.session.scalar(db.select(User).filter_by(username=field.data.strip())):
            raise ValidationError('Username already taken.')

    def validate_email(self, field):
        if db.session.scalar(db.select(User).filter_by(email=field.data.strip().lower())):
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')