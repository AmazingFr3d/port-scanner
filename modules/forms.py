from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from modules.models import User


class RegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email address')

    name = StringField(label="Full Name", validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label="Email Address", validators=[Email(), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label="Create Account")


class LoginForm(FlaskForm):
    email = StringField(label="Email Address", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Sign In")
