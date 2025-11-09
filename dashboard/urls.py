from django.urls import path
from . import views
from . import views as api

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),    
    path('dash/', views.dash, name='dash'),           

    # Ingredientes
    path('ingredientes/', api.ingredientes_list_create, name='ingredientes-list-create'),
    path('ingredientes/<str:ingrediente_id>/', api.ingrediente_detail, name='ingrediente-detail'),
    path('receitas/<str:receita_id>/ingredientes/', api.ingredientes_create_for_receita, name='ingredientes-create'),

    # Receitas
    path('receitas/', api.receitas_list_create, name='receitas-list-create'), # Listar Receitas
    path('receitas/<str:receita_id>/', api.receita_detail, name='receita-detail'), #  Detalhes, Atualizar, Deletar Receita



]