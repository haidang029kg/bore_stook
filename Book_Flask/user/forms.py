from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

from Book_Flask.models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', 
                        validators=[DataRequired(), Length(min=6, max=30)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing up')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken!')


class LoginForm(FlaskForm):
    email = StringField('Email',
							validators=[DataRequired(), Email()])
    password = PasswordField('Password',
							validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log in')