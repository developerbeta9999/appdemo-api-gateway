from django.urls import path
from .views import gateway_products

urlpatterns = [
    # Ruta vacía porque el prefijo 'api/products/' vendrá del core
    path('', gateway_products),
]
