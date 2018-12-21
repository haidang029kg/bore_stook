from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired




class AdmimLoginForm(FlaskForm):
    username = StringField('Admin Account:',
                    validators=[DataRequired()])
    password = PasswordField('Password:',
                    validators=[DataRequired()])
    submit = SubmitField('Log in')

