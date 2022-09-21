from django.urls import path, include
from ttoe.viewsets import MoveAPI

# importing views from views..py
from .views import home

urlpatterns = [
    path('', home ),
    path('api/move', MoveAPI.as_view() ),
]


