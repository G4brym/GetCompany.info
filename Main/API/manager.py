from django.contrib.auth.models import User
from django.utils.timezone import utc

import datetime
import json
import re

import Main.API.endpoints.actions as api_actions
import Main.API.endpoints.models as api_models

class api:
    # 1 => models only, default
    # 2 => actions
    __request_type = 1

    __result = None
    __errors = []
    __code = 0

    __request = None

    __user = None

    __endpoint_str = None
    __action_str = None

    # The actual endpoint inicialized
    __endpoint = None

    __input_data = None

    # Returns the final result
    def getResult(self):
        tmp_code = self.getCode()
        pattern = re.compile("[4]")
        if not pattern.match(str(tmp_code)):
            return {
                "data": self.__result,
                "code": self.__code
            }
        else:
            return {"errors": self.__errors,
                "code": self.__code
            }

    # Returns the code
    def getCode(self):
        return self.__code

    # Starts the class
    def __init__(self, request, endpoint, action):
        # Gets the request type and saves it
        if action.isdigit():
            self.__request_type = 1
        else:
            self.__request_type = 2

        # Saves the provided information
        self.__request = request
        self.__endpoint_str = endpoint
        self.__action_str = action

        # Starts the endpoint
        self.__code = self.__process()

    # Main process, where the magic happens
    def __process(self):
        # Try to get the endpoint
        try:
            if(self.__request_type == 1):
                self.__endpoint = getattr(api_models, str('api_model_' + self.__endpoint_str))(self.__request, self.__action_str, self.__input_data)
            else:
                self.__endpoint = getattr(api_actions, str('api_action_' + self.__endpoint_str))(self.__request, self.__action_str, self.__input_data)
        except AttributeError as e:
            # Returns not found
            self.__result = e
            print(e)
            return 404
        else:

            # checks if the endpoint requires an action and if the action was empty
            if self.__endpoint.requires_action() and self.__action_str == "":
                return 400

            # checks if the http method is allows in this endpoint
            if self.__request.method not in self.__endpoint.get_methods():
                return 405

            # Saves the POSTed data
            if self.__request.method in self.__endpoint.get_methods_require_info():
                self.__input_data = json.loads(self.__request.body.decode('utf-8'))
            else:
                self.__input_data = None

            # checks if the endpoint requires auth
            if self.__endpoint.requires_auth():

                # Try to get the auth key
                if self.__request.user.is_authenticated():

                    # Get the user
                    self.__user = self.__request.user

                # User is not authenticated
                else:
                    return 401

                # Saves the user
                self.__endpoint.set_user(self.__user)

            # Get the result from the endpoint
            result = self.__endpoint.getResult()

            # Saves the result
            self.__result = result["result"]
            self.__errors = result["errors"]
            return result["code"]