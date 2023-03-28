from typing import Optional

from celery import shared_task
from django.core.mail import send_mail

from authapp.models import User


# Функция отправки сообщения (обратная связь) из формы контактов
@shared_task
def send_feedback_to_email(message_body: str, message_from: int) -> None:
    if message_from is not None:
        user_from = User.objects.filter(pk=message_from).first().get_full_name()
    else:
        user_from = 'Аноним'

    send_mail(
        subject=f'Сообщение с сайта от: {user_from}',
        message=message_body,
        recipient_list=['support@braniac.local'],
        from_email='support@braniac.local',
        fail_silently=False
    )
