#!/usr/bin/env python3
"""Personal Data"""


import bcrypt


def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
