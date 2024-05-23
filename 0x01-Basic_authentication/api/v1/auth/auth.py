#!/usr/bin/env python3
""" Module of Authentication
"""
from typing import List, TypeVar
from flask import request


User = TypeVar('User')


class Auth:
    """
    Auth class. This class is the template for all authentication system.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to require authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """ Method to get authorization header """
        return None

    def current_user(self, request=None) -> User:
        """ Method to get current user """
        return None
