from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('query/<str:ticker>', views.get_data),
    # path('login/', views.login_user),
    # path('login/submit', views.submit_login),
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home),
    path('home/ativo/', views.ativo),
    path('home/ativo/?id=<int:id>', views.ativo),
    path('home/ativo/submit', views.submit_ativo),
    path('home/ativo/delete/<int:id>', views.deletar_ativo),
    # path('home/historico', views.visualizar_historico)

]
