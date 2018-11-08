from flask import url_for
from flask_mail import Message
from Book_Flask import mail


def send_token_email(user):
    token = user.get_reset_token()

    msg = Message('Password Reset Request',
                    sender = 'no-reply@gmail.com',
                    recipients = [user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('user.reset_passwd', token = token, _external = True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''

    mail.send(msg)