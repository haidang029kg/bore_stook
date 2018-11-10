from flask import url_for
from flask_mail import Message
from Book_Flask import mail
import uuid

def generate_id(type):
    id = str(uuid.uuid1())

    switcher = {
        'user' : str('user-' + id)[:16],
        'book' : str('book-' + id),
        'order' : str('order-' + id)[:16]
    }

    return switcher.get(type)



def send_token_reset(user):
    token = user.get_token()

    msg = Message('Password Reset Request',
                    sender = 'no-reply@gmail.com',
                    recipients = [user.Email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('user.reset_passwd', token = token, _external = True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''

    mail.send(msg)



def send_token_register(user):
    token = user.get_token()

    msg = Message('Activating Account',
                    sender = 'no-reply@gmmail.com',
                    recipients = [user.Email])
    
    msg.body = f'''To activate your account, click the following link to complete:
{url_for('user.register_token', token = token, _external = True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''

    mail.send(msg)