#!/usr/bin/env python
import json
import logging
import os
from http.client import HTTPSConnection
from urllib.parse import urlencode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

log = logging.getLogger("pushover")


class PushoverException(Exception):
    """
    This exception is to be thrown in when having issues
    """

    def __init__(self, message="generic problem"):
        self.message = message
        super().__init__(self.message)


class PushoverMessage:
    """
    Used for storing message specific data.
    """

    def __init__(self, message):
        """
        Creates a PushoverMessage object.
        """
        self.vars = {}
        self.vars["message"] = message

    def set(self, key, value):
        """
        Sets the value of a field "key" to the value of "value".
        """
        if value is not None:
            self.vars[key] = value

    def get(self):
        """
        Returns a dictionary with the values for the specified message.
        """
        return self.vars

    def user(self, user_token=None, user_device=None):
        """
        Sets a single user to be the recipient of this message with token "user_token" and device "user_device".
        """

        self.set("user", user_token)
        self.set("device", user_device)

    def __str__(self):
        return "PushoverMessage: " + str(self.vars)


class Pushover:
    """
    Creates a Pushover handler.

    Usage:

        po = Pushover("My App Token")
        po.user("My User Token", "My User Device Name")

        msg = po.msg("Hello, World!")

        po.send(msg)

    """

    PUSHOVER_SERVER = "api.pushover.net:443"
    PUSHOVER_ENDPOINT = "/1/messages.json"
    PUSHOVER_CONTENT_TYPE = {"Content-type": "application/x-www-form-urlencoded"}

    def __init__(
        self,
        app_token=None,
        user_token=None,
        device_token=None,
        title=None,
        message=None,
    ):
        """
        Creates a Pushover object.
        """

        # fatal if not set
        if app_token is None:
            # attempt to use environment variables if no token is provided.
            app_token = os.getenv("PUSHOVER_APP_TOKEN")
            if app_token is not None:
                log.info(f"found a value in PUSHOVER_APP_TOKEN to use")

        if app_token is None:
            raise PushoverException("No token supplied.")

        # fatal if not set
        if user_token is None:
            # attempt to use environment variables if no token is provided.
            user_token = os.getenv("PUSHOVER_USER_TOKEN")
            if user_token is not None:
                log.info(f"found a value in PUSHOVER_USER_TOKEN to use")

        if app_token is None:
            raise PushoverException("No app_token supplied.")

        # non-fatal if not set.
        if device_token is None:
            # attempt to use environment variables if no token is provided.
            device_token = os.getenv("PUSHOVER_DEVICE_TOKEN")
            if device_token is not None:
                log.info(f"found a value in PUSHOVER_DEVICE_TOKEN to use")

        self.app_token = app_token
        self.user_token = user_token
        self.user_device = None

        if message is not None:
            pom = PushoverMessage(message)
            if title is not None:
                pom.set("title", title)

            self.messages = [pom]

    def msg(self, message):
        """
        Creates a PushoverMessage object. Takes one "message" parameter (the message to be sent).
        Returns with PushoverMessage object (msg).
        """

        message = PushoverMessage(message)
        self.messages.append(message)
        return message


    def send(self):
        """
        Sends all PushoverMessage's owned by the Pushover object.
        """

        response = []
        for message in self.messages:
            response.append(self._send(message))
        return response

    def user(self, user_token, user_device=None):
        """
        Sets a single user to be the recipient of all messages created with this Pushover object.
        """

        self.user_token = user_token
        self.user_device = user_device

    def _send(self, message):
        """
        Sends the specified PushoverMessage object via the Pushover API.
        """

        kwargs = message.get()
        kwargs["token"] = self.app_token

        assert "message" in kwargs
        assert self.app_token is not None

        if not "user" in kwargs:
            if self.user is not None:
                kwargs["user"] = self.user_token
                if self.user_device is not None:
                    kwargs["device"] = self.user_device

        data = urlencode(kwargs)
        conn = HTTPSConnection(Pushover.PUSHOVER_SERVER)
        conn.request(
            "POST", Pushover.PUSHOVER_ENDPOINT, data, Pushover.PUSHOVER_CONTENT_TYPE
        )
        output = conn.getresponse().read().decode("utf-8")
        data = json.loads(output)

        if data["status"] != 1:
            raise PushoverException(output)
        else:
            return True
