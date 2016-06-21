from django.core import serializers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core import serializers

import json
import datetime
import re
import time

from Main.models import Companies, Tokens, CAE

class api_action_moreinfo:
    ###
    # Default content
    #
    __result = {}
    __errors = []
    __code = 500

    __requires_auth = False

    # Requires an ID
    __requires_action = False
    __allowed_methods = ["GET"]
    # Methods that require some sort of info posted, input
    __methods_require_info = []

    __request = None
    __id = None
    # Equal to self.__id but it is used by the manager so it can check if an id is required
    __action = None

    __user = None

    __input_data = None

    # returns if this endpoint requires auth
    def requires_auth(self):
        return self.__requires_auth

    # returns if this endpoint requires an action
    def requires_action(self):
        return self.__requires_action

    # returns the allowed methods of this endpoint
    def get_methods(self):
        return self.__allowed_methods

    # returns the allowed methods of this endpoint
    def get_methods_require_info(self):
        return self.__methods_require_info

    # Starts the endpoint
    def __init__(self, request, id, input_data):
        self.__request = request
        self.__id = id
        self.__action = id
        self.__input_data = input_data

    # Sets the user if this endpoint requires auth
    def set_user(self, user):
        self.__user = user

    # Returns the results
    def getResult(self):
        # Custom caller for users api
        if self.requires_action() and self.__id == "":
            self.__code = 404
        else:
            func = str(str(self.__request.method).lower() + '_process')
            self.__code = getattr(self, func)()

        return {"code": self.__code, "errors": self.__errors, "result": self.__result}
    #
    # End Default content
    ###

    def get_process(self):
        try:
            token_str = str(self.__request.GET.get("token")).strip()
        except AttributeError:
            return 400

        try:
            token = Tokens.objects.get(id=token_str)
        except Tokens.DoesNotExist:
            return 400

        if token.valid == False:
            return 400

        crawled = False
        for x in range(1, 10):
            company = Companies.objects.get(id=token.company_id)

            if company.already_crawled == True:
                crawled = True
                continue
            else:
                del company
                time.sleep(0.5)

        if crawled == False:
            return 504

        cae = CAE.objects.get(id=company.cae)

        result = {
            "address": company.address,
            "address_l2": company.address_l2,
            "phone": company.phone,
            "mobile": company.mobile,
            "fax": company.fax,
            "email": company.email,
            "info": company.info,
            "about": company.about,
            "products": company.products,
            "brands": company.brands,
            "tagss": company.tags,
            "links": company.links,
            "website": company.website,
            "facebook": company.facebook,
            "twitter": company.twitter,
            "linkedin": company.linkedin,
            "googleplus": company.googleplus,
            "active": company.active,
            "active_tab": company.active_tab,
            "cae_text": cae.text,
        }

        token.delete()
        self.__result = result

        return 200