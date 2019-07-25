from django.urls import path, include
from . import views


urlpatterns = [
    path('hotel/<str:hotelname>/', views.categories, name='cat-page-hotel'),
    path('airline/<str:airline>/', views.categories_airlines, name='cat-page-airline'),
]
