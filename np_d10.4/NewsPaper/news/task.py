from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.conf import settings
from .models import Post
from datetime import timedelta, date
from time import sleep

# from django.utils.timezone import datetime, timedelta, timezone, timestamp


def collect_subscribers(category):
    """
    iterate thro all subscribers in Category table, extract their email and form up a list of email recepients
    """
    email_recipients = []
    for user in category.subscribers.all():
        email_recipients.append(user.email)
    print(f'collect_subscribers func: {email_recipients}')
    return email_recipients


def send_emails(post_object, *args, **kwargs):
    # print(kwargs['template'])
    html = render_to_string(
        kwargs['template'],
        {'category_object': kwargs['category_object'], 'post_object': post_object},
        # передаем в шаблон любые переменные
    )
    print(kwargs)
    msg = EmailMultiAlternatives(
        subject=kwargs['email_subject'],
        from_email=settings.EMAIL_HOST_USER,
        to=kwargs['email_recipients']  # отправляем всем из списка
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)
