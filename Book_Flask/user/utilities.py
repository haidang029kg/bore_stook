from flask import url_for
from flask_mail import Message
from Book_Flask import mail, app
import secrets, os
from PIL import Image
from threading import Thread
from google.cloud import storage

SUB_URL = 'userava/'

def send_message(msg):
    with app.test_request_context():
        mail.send(msg)


def send_token_reset(user):
    token = user.get_token()

    msg = Message('Password Reset Request',
                    sender = 'no-reply@gmail.com',
                    recipients = [user.Email])
    
    msg.body = "To reset your password, visit the following link:\n{url_for('user.reset_passwd', token = token, _external = True)}\nIf you did not make this request then simply ignore this email and no changes will be made."

    myThread = Thread(target=send_message, args=(msg, ))
    myThread.start()


def save_picture(form_picture, old_file):
    randome_hex = secrets.token_hex(8)

    _, file_ext = os.path.splitext(form_picture.filename)

    new_pic_filename = randome_hex + file_ext

    client = storage.Client('final-thesis-100496')
    bucket = client.bucket('borestook')
    if (old_file != ''):
        blob = bucket.blob('userava/' + old_file)
        blob.delete()
    blob = bucket.blob('userava/' + new_pic_filename)
    blob.upload_from_string(form_picture.read(),content_type=form_picture.content_type)
	
    return new_pic_filename


def send_token_register(user):
    token = user.get_token()

    msg = Message('Activating Account',
                    sender = 'no-reply@gmmail.com',
                    recipients = [user.Email])
    
    msg.body = f'''Register completely, click link below to continue:
{url_for('user.register_token', token = token, _external = True)}
'''
    myThread = Thread(target=send_message, args=(msg, ))
    myThread.start()