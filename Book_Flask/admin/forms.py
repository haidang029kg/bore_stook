from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from Book_Flask import db
from Book_Flask.models import Author, Genre, Book

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
    author = SelectMultipleField('Author(s):', choices=db.session.query(Author.Name, Author.Name).all())
    publicationYear = StringField('Publication year:', validators=[
                                  DataRequired(), Length(min=1, max=4)])
    imgUrl = StringField('Image URL:', validators=[
                         DataRequired(), Length(min=1, max=100)])
    price = StringField('Price:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    avgRating = StringField('Rating:', validators=[
                            DataRequired(), Length(min=1, max=3)])
    quantity = StringField('Quantity:', validators=[
                           DataRequired(), Length(min=1, max=4)])
    genre = SelectField('Genre:', choices=db.session.query(Genre.GenreID, Genre.Name).all(), coerce=int)
    submit = SubmitField('Add book')


    def validate_ISBN(self, ISBN):
        book = Book.query.filter_by(ISBN = ISBN.data).first()
        print('1111111111111111111')
        print(ISBN)

        if book:
            raise ValidationError('This ISBN exists already!!!')
