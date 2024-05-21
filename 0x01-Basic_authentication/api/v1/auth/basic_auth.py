#!/usr/bin/env python3
""" Basic Authentication module
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar

class BasicAuth(Auth):
    """ BasicAuth class that inherits from Auth """

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Retrieve User instance based on email and password """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
