from flask_mail import Message
from flask import current_app, render_template
from . import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target = send_async_email, args=[current_app, msg])
    thr.start()
    return thr
