from django.core import serializers
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core import serializers

import json
import datetime
import re

from Main.models import Companies, CAE

class api_action_search:
    ###
    # Default content
    #
    __result = {"data": []}
    __errors = []
    __code = 500

    __requires_auth = False

    # Requires an ID
    __requires_action = False
    __allowed_methods = ["POST"]
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

    def post_process(self):
        try:
            query = str(self.__request.POST.get("q")).strip()
        except AttributeError:
            return 400

        if len(query) < 3:
            return 411

        if query.isdigit():
            search = Companies.objects.filter(identifier__contains=str(query), active=True).order_by('active', '-state')[:15]

            tmp = []
            for company in search:
                tmp.append({"identifier": company.identifier, "name": company.name, "state": company.state})

            self.__result = tmp
        else:
            search = Companies.objects.filter(name__icontains=str(query), active=True).order_by('active', '-state')[:15]

            tmp = []
            for company in search:
                tmp.append({"identifier": company.identifier, "name": company.name, "state": company.state})

            self.__result = tmp

        if(len(self.__result) == 0):
            return 404

        return 200