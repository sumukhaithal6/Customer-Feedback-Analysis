from django.urls import path, include
from . import views


urlpatterns = [
    path('<str:hotelname>/', views.categories, name='cat-page'),
]
