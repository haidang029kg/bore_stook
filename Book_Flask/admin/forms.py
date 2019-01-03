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
    author = SelectMultipleField(
        'Author(s):', choices=db.session.query(Author.Name, Author.Name).all())
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
    genre = SelectField('Genre:', choices=db.session.query(
        Genre.GenreID, Genre.Name).all(), coerce=int)

    submit = SubmitField('Add book')

    def validate_ISBN(self, ISBN):
        book = Book.query.filter_by(ISBN=ISBN.data).first()

        if book:
            raise ValidationError('This ISBN exists already!!!')


class EditBookForm(FlaskForm):
    title = StringField('Book title:', validators=[
                        DataRequired(), Length(min=1, max=30)])
    ISBN = StringField('ISBN:', validators=[
                       DataRequired(), Length(min=10, max=13)])
    author = SelectMultipleField('Author(s):', choices=db.session.query(
        Author.Name, Author.Name).all(), default=['2'])
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
    genre = SelectField('Genre:', choices=db.session.query(
        Genre.GenreID, Genre.Name).all(), coerce=int)

    submit = SubmitField('Edit book')

    def validate_ISBN(self, ISBN):
        book = Book.query.filter_by(ISBN = ISBN.data).first()
        # it is the current book
        if book:
            # another book
            id_current_book = book.BookID
            book_2 = db.session.query(Book.BookID).filter(Book.ISBN == ISBN.data).filter(Book.BookID != id_current_book).first()
            if book_2:
                raise ValidationError('This ISBN already exists!!!')


class AddAuthorForm(FlaskForm):
    name = StringField('Author Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        author = db.session.query(Author.AuthorID).filter(Author.Name == name.data).first()
        
        if author:
            raise ValidationError('This author already exists!!!')




class AddGenreForm(FlaskForm):
    name = StringField('Genre Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        genre = Genre.query.filter_by(Name=name.data).first()
        if genre:
            raise ValidationError('This genre already exists!!!')
