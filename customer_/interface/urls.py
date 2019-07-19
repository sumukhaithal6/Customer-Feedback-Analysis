from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hotel, name='hotel-int'),
    # path('inter/', views.interface, name='interface-page'),
]
