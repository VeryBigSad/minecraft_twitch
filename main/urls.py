from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='authorise_with_twitch'),
]
