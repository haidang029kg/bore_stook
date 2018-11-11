from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email

from Book_Flask.models import User

class RegistrationForm(FlaskForm):
    fname = StringField('First Name', 
                        validators=[DataRequired(), Length(min=1, max=30)])
    lname = StringField('Last Name', 
                        validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing up')
    
    def validate_email(self, email):
        user = User.query.filter_by(Email = email.data).first()
        if user:
            raise ValidationError('That email is taken!')



class ChangePasswdForm(FlaskForm):
    current_password = PasswordField('Current Password',
                                    validators=[DataRequired()])
    password = PasswordField('New Password',
                                    validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change')



class LoginForm(FlaskForm):
    email = StringField('Email',
							validators=[DataRequired(), Email()])
    password = PasswordField('Password',
							validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Log in')


class RequestPasswdForm(FlaskForm):
    email = StringField('Email',
                            validators = [DataRequired(), Email()])
    submit = SubmitField('Request')


    def validate_email(self, email):
        user = User.query.filter_by(Email = email.data).first()

        if user is None:
            raise ValidationError('There is no account with this email!')



class ResetPasswdForm(FlaskForm):
    password = PasswordField('Password',
                                validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


class AccountForm(FlaskForm):
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])

    fname = StringField('First Name', 
                        validators=[DataRequired(), Length(min=1, max=30)])
    lname = StringField('Last Name', 
                        validators=[DataRequired(), Length(min=1, max=30)])
    phone = StringField('Phone')

    submit = SubmitField('Change')

    def validate_phone(self, phone):
        if (type(int(phone.data)) != type(123)):
            raise ValidationError('Phone number is incorrect!')