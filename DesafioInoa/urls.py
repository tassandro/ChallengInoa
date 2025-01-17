from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='home/')),
    path('home/', views.home),
    path('home/ativo/', views.ativo),
    path('home/ativo/?id=<int:id>', views.ativo),
    path('home/ativo/submit', views.submit_ativo),
    path('home/ativo/delete/<int:id>', views.deletar_ativo),
    path('obter_cotacoes/<int:id>', views.obter_cotacoes)

]
