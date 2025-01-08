from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import requests
# Create your views here.

API_URL = 'https://brapi.dev/api/quote/'
API_KEY = '6s4xhTzigCC6bbdpf6Pk3Z'

def get_data(request, ticker):
    url = f'{API_URL}{ticker}?token={API_KEY}'
    print(url)
    r = requests.get(url)
    data = r.json()

    return JsonResponse(data)


def home(request):
    return HttpResponse("<h1>Home</h1>")