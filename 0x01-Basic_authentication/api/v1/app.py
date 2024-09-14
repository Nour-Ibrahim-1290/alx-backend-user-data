#!/usr/bin/env python3
"""
Route module for the API.

This module sets up the Flask application, registers blueprints, and configures
CORS. It also handles authentication based on the `AUTH_TYPE` environment variable
and defines error handlers for common HTTP errors.
"""

from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os

# Initialize Flask application
app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Configure authentication
auth = None
if os.getenv('AUTH_TYPE') == 'basic_auth':
    auth = BasicAuth()
else:
    auth = Auth()

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    Returns a JSON response with a 404 status code.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    Returns a JSON response with a 401 status code.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    Returns a JSON response with a 403 status code.
    """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request_func():
    """
    This function is executed before each request to the API.
    It checks if the `auth` object requires authentication for the request path.
    If authentication is required, it verifies the authorization header and the current user.
    """
    if auth is None:
        return
    if not auth.require_auth(
            request.path,
            ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
            ):
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

if __name__ == "__main__":
    # Get host and port from environment variables, with default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
