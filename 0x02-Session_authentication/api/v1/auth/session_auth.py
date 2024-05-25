#!/usr/bin/env python3
""" Module of Sesion Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, List
import base64
import uuid


class SessionAuth(Auth):
    """ Session Authentication Module
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id
        """
        if user_id is None or type(user_id) != str:
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id