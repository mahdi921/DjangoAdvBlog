from celery import shared_task
from time import sleep


@shared_task
def send_email():
    sleep(5)
    print("Email sent!")
