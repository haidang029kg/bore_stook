from flask import url_for
from flask_mail import Message
from Book_Flask import mail, app
import secrets
import os
from PIL import Image
from threading import Thread


def send_message(msg):
    with app.test_request_context():
        mail.send(msg)


def send_token_reset(user):
    token = user.get_token()

    msg = Message('Password Reset Request',
                  sender='no-reply@gmail.com',
                  recipients=[user.Email])

    msg.body = f'''To reset your password, visit the following link:
{url_for('user.reset_passwd', token = token, _external = True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''

    myThread = Thread(target=send_message, args=(msg, ))
    myThread.start()


def save_picture(form_picture):
    randome_hex = secrets.token_hex(8)

    _, file_ext = os.path.splitext(form_picture.filename)
    new_pic_filename = randome_hex + file_ext
    pic_path = os.path.join(
        app.root_path, 'static/image/profile_user_pic', new_pic_filename)
    # pic_path will be changed to the appropriate cloud store on gcloud

    output_pic_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_pic_size)
    i.save(pic_path)

    return new_pic_filename


def send_token_register(user):
    token = user.get_token()

    msg = Message('Activating Account',
                  sender='no-reply@gmmail.com',
                  recipients=[user.Email])

    msg.body = f'''Register completely, click link below to continue:
{url_for('user.register_token', token = token, _external = True)}
'''
    myThread = Thread(target=send_message, args=(msg, ))
    myThread.start()
