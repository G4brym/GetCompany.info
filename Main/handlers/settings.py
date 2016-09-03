# Created by Gabriel Massadas on 23-12-2015.
import os

AUTH_SETTINGS = {
    "max_tries_per_minute": 15
}

RECAPTCHA_SECRET_KEY = '6Ldg1BgTAAAAAFpgDqOa9XqE0UqHEw5fpXSDx9aR'

MAX_COMPANIES = 700000

def get_DEBUG():
    if(int(os.environ.get('DEBUG')) == 1):
        return True
    else:
        return False
        
def is_bot(request):
    if("bot" in str(request.META['HTTP_USER_AGENT']).lower()):
        return True
    else:
        return False