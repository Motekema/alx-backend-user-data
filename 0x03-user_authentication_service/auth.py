#!/usr/bin/env python3
import bcrypt
from uuid import uuid4
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt and returns it as bytes."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def _generate_uuid() -> str:
    """Generates a new UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user if the email does not exist."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided credentials are valid."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for the user with the given email."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Returns the user associated with the given session ID."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session of the given user."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for the user."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password for the user with the given reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user
            (user.id, hashed_password=hashed_password, reset_token=None)
        except NoResultFound:
            raise ValueError
