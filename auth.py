"""Simple username/password authentication (salted PBKDF2 hashes)."""
import hashlib
import os

import db


def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000).hex()


def register(username, password):
    if not username or not password:
        return False, "Username and password are required."
    if db.get_user(username):
        return False, "Username already exists."
    salt = os.urandom(16).hex()
    db.add_user(username, salt, _hash(password, salt))
    return True, "Registered. You can now log in."


def login(username, password):
    user = db.get_user(username)
    return bool(user) and user["password_hash"] == _hash(password, user["salt"])
