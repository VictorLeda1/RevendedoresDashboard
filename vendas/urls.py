from django.urls import path
from . import views

urlpatterns = [
    path('nova/', views.nova_venda_view, name='nova_venda'),
]
