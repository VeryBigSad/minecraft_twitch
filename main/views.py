import string

import requests

from django.db import IntegrityError
from django.shortcuts import render

from felix_twitch.settings import DOMAIN_NAME
from main.models import Player


def index(request):
    channel_id = '423486275'

    if request.method == 'POST':
        username = request.POST['mc-username']
        print(username)

        # username validation
        for i in username:
            if i.upper() not in string.ascii_uppercase + '0123456789_':
                # raise ValidationError
                raise Exception('Юзернейм неверен.')

        twitch_id = request.POST.get('id')
        obj = Player.objects.get(twitch_id=twitch_id, mc_username=None)
        obj.mc_username = username
        obj.save()
        return render(request, 'thanks.html', context={'username': username})

        # TODO: username at thanks.html

    else:
        if request.GET.get('code'):
            # getting user information
            resp = requests.post('https://id.twitch.tv/oauth2/token', data={
                'client_id': 'geqwz9a4dhcg3wcmv8qsu07p5bb9cx',
                'client_secret': '37cs0vpf6k3l3s71d3e8ios99ql6wi',
                'code': request.GET.get('code'),
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://' + DOMAIN_NAME,
            }).json()
            access_token = resp.get('access_token')
            if not access_token:
                return render(request, '500.html', context={'title': 'Ошибка, попробуйте переавторизоваться.'})
            headers = {'Accept': 'application/vnd.twitchtv.v5+json',
                       'Client-ID': 'geqwz9a4dhcg3wcmv8qsu07p5bb9cx',
                       'Authorization': 'OAuth %s' % access_token}
            user_id = requests.get('https://api.twitch.tv/helix/users',
                                   headers=
                                   {'Accept': 'application/vnd.twitchtv.v5+json',
                                    'Client-ID': 'geqwz9a4dhcg3wcmv8qsu07p5bb9cx',
                                    'Authorization': 'Bearer %s' % access_token}).json().get('data')[0].get('id')

            # checking if he is subbed
            resp2 = requests.get('https://api.twitch.tv/kraken/users/%s/subscriptions/%s' % (user_id, channel_id),
                                 headers=headers).json()
            if resp2.get('status') == 404:
                return render(request, 'not_subbed.html', context={'debug': str([resp, resp2])})

            obj = Player(twitch_id=user_id, mc_username=None)
            try:
                obj.save()
            except IntegrityError:
                if not Player.objects.filter(twitch_id=user_id, mc_username=None).exists():
                    return render(request, '500.html', context={'title': 'Ты уже добавлен в вайтлист.'})
            return render(request, 'add.html', context={'twitch_id': user_id})
        return render(request, 'index.html', context={'test_id': channel_id})
