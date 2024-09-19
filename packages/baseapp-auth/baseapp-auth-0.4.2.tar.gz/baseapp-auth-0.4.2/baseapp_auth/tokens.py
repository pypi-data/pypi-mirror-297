from math import floor

from baseapp_core.tokens import TokenGenerator
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import timedelta


class ChangeEmailConfirmTokenGenerator(TokenGenerator):
    key_salt = "change-email"

    def get_signing_value(self, user):
        return [user.id, user.new_email, user.is_new_email_confirmed]


class ChangeEmailVerifyTokenGenerator(TokenGenerator):
    key_salt = "verify-email"

    def get_signing_value(self, user):
        return [user.id, user.new_email, user.is_new_email_confirmed]


class ConfirmEmailTokenGenerator(TokenGenerator):
    key_salt = "confirm_email"

    def get_signing_value(self, user):
        return [user.pk, user.email]


class PreAuthTokenGenerator(TokenGenerator):
    key_salt = "pre_auth_token"

    def get_signing_value(self, user):
        return [user.pk, user.email]

    @property
    def max_age(self) -> int | None:
        if hasattr(settings, "BA_AUTH_PRE_AUTH_TOKEN_EXPIRATION_TIME_DELTA"):
            _time_delta = settings.BA_AUTH_PRE_AUTH_TOKEN_EXPIRATION_TIME_DELTA
            if not isinstance(_time_delta, timedelta):
                raise ImproperlyConfigured(
                    "BA_AUTH_PRE_AUTH_TOKEN_EXPIRATION_TIME_DELTA must be a timedelta"
                )
            return int(floor(_time_delta.total_seconds()))
        return None


class ChangeExpiredPasswordTokenGenerator(TokenGenerator):
    key_salt = "change_expired_password_token"

    def get_signing_value(self, user):
        return [user.pk, user.email]

    @property
    def max_age(self) -> int | None:
        if (
            time_delta := getattr(
                settings, "BA_AUTH_CHANGE_EXPIRED_PASSWORD_TOKEN_EXPIRATION_TIME_DELTA", None
            )
        ) and isinstance(time_delta, timedelta):
            return int(floor(time_delta.total_seconds()))
        raise ImproperlyConfigured(
            "BA_AUTH_CHANGE_EXPIRED_PASSWORD_TOKEN_EXPIRATION_TIME_DELTA must be a timedelta"
        )
