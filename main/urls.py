from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='authorise_with_twitch'),
    # path('fuckoff', name='not_twitch_sub'),
    # path('enter_mc_name', name='enter_mc_name')
]
