from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email


class AdminLoginForm(FlaskForm):
    email = StringField('email:',
                             validators=[DataRequired(), Email()])
    password = PasswordField('password:',
                             validators=[DataRequired()])
    submit = SubmitField('Log in')


class AddBookForm(FlaskForm):
    title = StringField('Book title:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    ISBN = StringField('ISBN:', validators=[
                       DataRequired(), Length(min=10, max=13)])
    author = StringField('Author:', validators=[
                         DataRequired(), Length(min=1, max=300)])
    publicationYear = StringField('Publication year:', validators=[
                                  DataRequired(), Length(min=1, max=4)])
    imgUrl = StringField('Image URL:', validators=[
                         DataRequired(), Length(min=1, max=30)])
    price = StringField('Price:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    avgRating = StringField('Rating:', validators=[
                            DataRequired(), Length(min=1, max=1)])
    quantity = StringField('Quantity:', validators=[
                           DataRequired(), Length(min=1, max=4)])
    genre = StringField('Genre:', validators=[
                        DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Add book')
