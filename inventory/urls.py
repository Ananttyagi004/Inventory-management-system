from django.urls import path
from .views import ItemView  # Adjust the import according to your project structure

urlpatterns = [
    path('items/', ItemView.as_view(), name='create_items'),  # For POST requests
    path('items/<str:sku>/', ItemView.as_view(), name='item_detail'),  # For GET, PUT, DELETE requests
]
