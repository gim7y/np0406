from django.db.models.signals import m2m_changed, post_save  # , post_save,
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives

from .models import PostCategory, Post, Category
from django.template.loader import render_to_string


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(post_save, sender=PostCategory)
def notify_subscribers(sender, instance, created, **kwargs):
    category = instance.categoryThrough
    post = instance.postThrough
    for sub in category.subscribers.all():
        html_content = render_to_string(
            "mail.html",
            {
                "post": post,
            },
        )
        msg = EmailMultiAlternatives(
            subject=f"{post.title}",
            body=post.text,
            from_email="gm_m@mail.ru",
            to=[sub.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
