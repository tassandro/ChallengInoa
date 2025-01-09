from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from core.forms import LoginForm, CreateAtivo
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
    user = request.user
    return render(request, 'model-page.html', {"user": user})


def login_user(request):
    return render(request, 'login.html', {'form': LoginForm()})

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Login inválido! Tente novamente.")
            return redirect('/login/')
    return redirect('/')