import requests
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.shortcuts import render

User = get_user_model()


def index(request):
    if request.method == 'POST':
        pass
    else:
        if request.GET.get('code'):
            channel_id = '423486275'

            # getting user information
            resp = requests.post('https://id.twitch.tv/oauth2/token', data={
                'client_id': 'geqwz9a4dhcg3wcmv8qsu07p5bb9cx',
                'client_secret': '37cs0vpf6k3l3s71d3e8ios99ql6wi',
                'code': request.GET.get('code'),
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost',
            }).json()
            access_token = resp.get('access_token')
            if not access_token:
                raise Http404
            headers = {'Accept': 'application/vnd.twitchtv.v5+json',
                       'Client-ID': 'geqwz9a4dhcg3wcmv8qsu07p5bb9cx',
                       'Authorization': 'OAuth %s' % access_token}
            user_id = requests.get('https://api.twitch.tv/kraken/user', headers=headers).json()['_id']
            print(user_id)

            # checking if he is subbed
            resp = requests.get('https://api.twitch.tv/kraken/users/%s/subscriptions/%s' % (user_id, channel_id),
                                headers=headers).json()
            if resp.get('status') == 404:
                return render(request, 'not_subbed.html')
            # removing our access because wont be using token anymore
            requests.post('https://id.twitch.tv/oauth2/revoke?client_id=geqwz9a4dhcg3wcmv8qsu07p5bb9cx&token=%s' %
                          request.GET.get('code'))
            return render(request, 'add.html')
        return render(request, 'index.html')
