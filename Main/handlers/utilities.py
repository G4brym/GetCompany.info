import uuid
import datetime as dt
import json
import urllib.request
import urllib.parse

from Main.handlers.settings import RECAPTCHA_SECRET_KEY


def get_title(title=""):
    if title == "":
        return "GetCompany info"
    else:
        return title + " - GetCompany info"

def get_new_token():
    return str(str(uuid.uuid4()) + str(uuid.uuid4())).replace("-", "")[:32]

def get_timestamp(datetime):
    return int(dt.datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S.%f").timestamp())

def remove_microseconds(datetime):
    return dt.datetime.strptime(datetime, "%Y-%m-%d %H:%M:%S.%f")

def get_remote_IP(request):
    ip = request.META.get('HTTP_CF_CONNECTING_IP')
    if ip is None:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def check_recaptcha(response, ip):
    if response == "":
        return False

    data = urllib.parse.urlencode({"secret": RECAPTCHA_SECRET_KEY, "response": response, "remoteip": ip})
    binary_data = data.encode('utf-8')
    u = urllib.request.urlopen("https://www.google.com/recaptcha/api/siteverify", binary_data)
    result = u.read()
    recaptcha_result = json.loads(result.decode('utf-8'))

    return recaptcha_result["success"]
