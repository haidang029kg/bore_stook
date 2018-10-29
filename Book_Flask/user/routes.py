from flask import Blueprint, render_template, url_for, flash, redirect, request

from Book_Flask import db, bcrypt
from Book_Flask.models import User
from Book_Flask.user.forms import RegistrationForm


user = Blueprint('user', __name__)

@user.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(email = form.email.data,
                    name = form.name.data, 
                    password = hashed_password)
        
        db.session.add(user)
        db.session.commit()
            
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.home'))
    
    return render_template('register.html', title = 'Register', form = form)