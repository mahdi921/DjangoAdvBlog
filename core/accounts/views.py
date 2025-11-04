from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from accounts.task import send_email
import requests

# Create your views here.


def send_email_view(request):
    send_email()
    return HttpResponse("<h1>Email Sent!</h1>")


@cache_page(60)
def test(request):
    response = requests.get(
        "https://324f61ec-07ad-4ef2-aecf-f8f8e196e353.mock.pstmn.io/test/delay/6")
    return JsonResponse(response.json())
