from django.urls import path, include
from . import views

urlpatterns = [
    path('hotels/', views.hotel, name='hotel-int'),
    path('airlines/', views.airline, name='airline-int')
    # path('inter/', views.interface, name='interface-page'),
]
