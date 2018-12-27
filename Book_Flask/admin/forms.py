from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from Book_Flask import db
from Book_Flask.models import Author, Genre

class AdmimLoginForm(FlaskForm):
    username = StringField('Admin Account:',
                           validators=[DataRequired()])
    password = PasswordField('Password:',
                             validators=[DataRequired()])
    submit = SubmitField('Log in')


class AddBookForm(FlaskForm):
    title = StringField('Book title:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    ISBN = StringField('ISBN:', validators=[
                       DataRequired(), Length(min=10, max=13)])
    author = SelectMultipleField('Author(s):', choices=db.session.query(Author.Name, Author.Name).all())
    publicationYear = StringField('Publication year:', validators=[
                                  DataRequired(), Length(min=1, max=4)])
    imgUrl = StringField('Image URL:', validators=[
                         DataRequired(), Length(min=1, max=100)])
    price = StringField('Price:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    avgRating = StringField('Rating:', validators=[
                            DataRequired(), Length(min=1, max=1)])
    quantity = StringField('Quantity:', validators=[
                           DataRequired(), Length(min=1, max=4)])
    genre = SelectField('Genre:', choices=db.session.query(Genre.GenreID, Genre.Name).all(), coerce=int)
    submit = SubmitField('Add book')
