#!/usr/bin/env python3
""" Module of Authentication
"""
from typing import List, TypeVar
from flask import request
import os


User = TypeVar('User')


class Auth:
    """
    Auth class. This class is the template for all authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to require authentication """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a '/'
        if not path.endswith('/'):
            path += '/'

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> User:
        """ Method to get current user """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        else:
            session_name = os.getenv('SESSION_NAME')
            return request.cookies.get(session_name)
