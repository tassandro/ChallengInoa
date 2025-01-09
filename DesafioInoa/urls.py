from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('query/<str:ticker>', views.get_data),
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),

]
