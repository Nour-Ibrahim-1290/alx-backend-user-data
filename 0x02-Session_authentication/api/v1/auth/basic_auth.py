#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, List
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

    def extract_user_credentials(
            self,
            decoded_base64_auth_header: str
            ) -> (str, str):
        """ Method to extract the user email and password
        from Base64 decoded string
        """
        if decoded_base64_auth_header is None \
                or ':' not in decoded_base64_auth_header:
            return None, None

        credentials = decoded_base64_auth_header.split(':', 1)
        user_email = credentials[0]
        user_pwd = credentials[1] if len(credentials) > 1 else None

        return user_email, user_pwd

    def user_object_from_credentials(
                self,
                user_email: str,
                user_pwd: str
                ) -> TypeVar('User'):
        """ Method to return the User instance
        based on his email and password
        """
        if user_email is None or type(
                user_email) is not str or user_pwd is None or type(
                user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to retrieve the User instance for a request """
        authorization_header = self.authorization_header(request)
        base64_authorization_header = self.extract_base64_authorization_header(
                                            authorization_header)
        decoded_base64_auth_header = self.decode_base64_authorization_header(
                                                base64_authorization_header)

        if decoded_base64_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                                decoded_base64_auth_header)

        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)

    def require_auth(
            self,
            path: str,
            excluded_paths: List[str]
            ) -> bool:
        """ Method to determine if path requires authentication """
        if path is None or excluded_paths is None \
                or len(excluded_paths) == 0:
            return True

        # Ensure path ends with '/'
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            # Remove wildcard character if present
            if excluded_path[-1] == '*':
                excluded_path = excluded_path[:-1]

            if path.startswith(excluded_path):
                return False

        return True
