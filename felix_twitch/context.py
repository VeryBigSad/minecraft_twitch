from felix_twitch.settings import DOMAIN_NAME


def domain_name(request):
    return {'DOMAIN_NAME': DOMAIN_NAME}
