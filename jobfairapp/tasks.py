# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_username_password_email(email):
    subject = 'Exam Login Details'
    message = 'Here are your username and password details for the exam.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
