from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),               
    # API endpoints (JSON)
    path('api/rotulos/', views.rotulos_list, name='rotulos_list'),   # GET list, POST create
    path('api/rotulos/<string:id>/', views.rotulos_detail, name='rotulos_detail'), # GET/PUT/DELETE
    path('api/indicadores/', views.indicadores, name='indicadores'), # indicadores para gráficos
]