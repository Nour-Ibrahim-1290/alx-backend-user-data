#!/usr/bin/env python3
""" Module of Sesion Authentication
"""
from flask import Flask, request, jsonify, make_response
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, List
from api.v1.views import app_views
from os import getenv
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id) != str:
            return None
        else:
            return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    @app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
    def login():
        email = request.form.get('email')
        if not email:
            return jsonify({"error": "email missing"}), 400

        password = request.form.get('password')
        if not password:
            return jsonify({"error": "password missing"}), 400

        users = User.search({'email': email})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404

        for user in users:
            if user.is_valid_password(password):
                from api.v1.app import auth
                session_id = auth.create_session(user.id)
                response = make_response(user.to_json())
                response.set_cookie(getenv('SESSION_NAME'), session_id)
                return response

        return jsonify({"error": "wrong password"}), 401
