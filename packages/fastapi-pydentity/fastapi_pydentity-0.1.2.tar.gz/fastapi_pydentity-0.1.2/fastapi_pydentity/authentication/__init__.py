from collections.abc import Callable
from datetime import timedelta
from typing import overload

from fastapi import FastAPI
from pydenticore import IdentityConstants
from pydenticore.authentication import (
    AuthenticationError,
    AuthenticationOptions,
    AuthenticationScheme,
    AuthenticationSchemeBuilder,
)
from pydenticore.authentication.interfaces import (
    IAuthenticationDataProtector,
    IAuthenticationOptionsAccessor,
    IAuthenticationSchemeProvider,
)
from starlette.responses import PlainTextResponse
from starlette.types import ExceptionHandler

from fastapi_pydentity.authentication.bearer import JWTBearerAuthenticationHandler, TokenValidationParameters
from fastapi_pydentity.authentication.cookie import CookieAuthenticationOptions, CookieAuthenticationHandler
from fastapi_pydentity.authentication.middlewares import AuthenticationMiddleware
from fastapi_pydentity.infrastructure import services


def use_authentication(app: FastAPI, on_error: ExceptionHandler | None = None) -> None:
    options = services.get(AuthenticationOptions)()
    accessor = services.get(IAuthenticationOptionsAccessor)(options)
    schemes = services.get(IAuthenticationSchemeProvider)(accessor)

    app.add_middleware(AuthenticationMiddleware, schemes=schemes)

    if on_error:
        app.add_exception_handler(AuthenticationError, on_error)
    else:
        app.add_exception_handler(
            AuthenticationError,
            lambda req, exc: PlainTextResponse("Unauthorized", status_code=401)
        )


class AuthenticationBuilder:
    """Used to configure authentication."""

    __slots__ = ("_options",)

    def __init__(self, options: AuthenticationOptions) -> None:
        self._options = options

    @overload
    def add_scheme(self, name: str, scheme: AuthenticationScheme) -> "AuthenticationBuilder":
        """
        Adds a ``AuthenticationScheme``.

        :param name: The name of this scheme.
        :param scheme:
        :return:
        """

    @overload
    def add_scheme(
            self,
            name: str,
            configure_scheme: Callable[[AuthenticationSchemeBuilder], None]
    ) -> "AuthenticationBuilder":
        """
        Adds a ``AuthenticationScheme``.

        :param name: The name of this scheme.
        :param configure_scheme:
        :return:
        """

    def add_scheme(
            self,
            name: str,
            scheme_or_builder: AuthenticationScheme | Callable[[AuthenticationSchemeBuilder], None],
    ) -> "AuthenticationBuilder":
        self._options.add_scheme(name, scheme_or_builder)
        return self

    def add_cookie(
            self,
            scheme: str = "Cookie",
            options: CookieAuthenticationOptions | None = None
    ) -> "AuthenticationBuilder":
        """
        Adds cookie authentication to ``AuthenticationBuilder`` using the specified scheme.

        :param scheme: The authentication scheme.
        :param options:
        :return:
        """
        return self.add_scheme(scheme, AuthenticationScheme(scheme, CookieAuthenticationHandler(options)))

    def add_cookie_data_protector(self, protector: IAuthenticationDataProtector) -> "AuthenticationBuilder":
        for scheme in self._options.scheme_map.values():
            if issubclass(type(scheme.handler), CookieAuthenticationHandler):
                scheme.handler.protector = protector
        return self

    def add_identity_cookies(self) -> "AuthenticationBuilder":
        self.add_cookie(IdentityConstants.ApplicationScheme)
        self.add_cookie(IdentityConstants.ExternalScheme, CookieAuthenticationOptions(timespan=timedelta(minutes=10)))
        self.add_cookie(IdentityConstants.TwoFactorRememberMeScheme)
        self.add_cookie(IdentityConstants.TwoFactorUserIdScheme)
        return self

    def add_jwt_bearer(
            self,
            scheme: str = "Bearer",
            *,
            validation_parameters: TokenValidationParameters
    ) -> "AuthenticationBuilder":
        """
        Enables JWT-bearer authentication using the default scheme 'Bearer'.

        :param scheme: The authentication scheme.
        :param validation_parameters:
        :return:
        """
        self.add_scheme(scheme, AuthenticationScheme(scheme, JWTBearerAuthenticationHandler(validation_parameters)))
        return self
