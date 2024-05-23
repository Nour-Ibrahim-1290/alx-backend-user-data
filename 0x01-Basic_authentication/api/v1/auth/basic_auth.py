#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ BasicAuth class.
    """
    def extract_base64_authorization_header(
                self,
                authorization_header: str
                ) -> str:
        """ Method to extract the Base64 Authorization """
        if authorization_header is None or type(
                        authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Method to decode the Base64 Authorization """
        if base64_authorization_header is None or type(
                base64_authorization_header) is not str:
            return None
        try:
            message_bytes = base64.b64decode(base64_authorization_header)
            message = message_bytes.decode('utf-8')
            return message
        except base64.binascii.Error:
            return None
