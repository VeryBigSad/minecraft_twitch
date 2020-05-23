from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include


def red_to_index(request):
    return redirect('authorise_with_twitch')


urlpatterns = [
    # path('admin-panel/', admin.site.urls),
    path('login', include('main.urls')),
    path('', red_to_index)
]

handler500 = 'felix_twitch.views.handler500'
handler404 = 'felix_twitch.views.handler404'
