#!/usr/bin/env python3
"""Personal Data"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if a provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
