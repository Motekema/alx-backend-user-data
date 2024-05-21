#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class for API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method to check if authentication is required """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure trailing slash consistency
        if path[-1] != '/':
            path += '/'

        for ex_path in excluded_paths:
            if ex_path[-1] != '/':
                ex_path += '/'
            if path == ex_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method to get the authorization header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method to get the current user """
        return None
