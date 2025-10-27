from django.http import HttpResponse
from accounts.task import send_email
# Create your views here.


def send_email_view(request):
    send_email()
    return HttpResponse("<h1>Email Sent!</h1>")
