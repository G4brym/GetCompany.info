import os, tweepy, random
from django.conf import settings

def send_update(company):
    auth = tweepy.OAuthHandler(str(os.environ.get('TWITTER_CONS_KEY')), str(os.environ.get('TWITTER_CONS_SEC')))
    auth.set_access_token(str(os.environ.get('TWITTER_ACESS_TOK')), str(os.environ.get('TWITTER_ACESS_SEC')))
    api = tweepy.API(auth)

    # todo check company country

    frase = "We got new information about %s at https://www.getcompany.info/%s/" % (company.name, company.identifier)

    if (True):

        fn = os.path.join(settings.BASE_DIR, 'Main/handlers/twitter/update/' + str(random.randint(0,5)) + ".jpg")

        api.update_with_media(fn, status=frase)