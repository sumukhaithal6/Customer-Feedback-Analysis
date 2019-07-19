from django.urls import path, include
from . import views

urlpatterns = [
    path('dummy/', views.home, name='dummy-home-page'),
    path('', views.landing, name='landing-page'),
    path('inter/', views.interface, name='interface-page'),
]