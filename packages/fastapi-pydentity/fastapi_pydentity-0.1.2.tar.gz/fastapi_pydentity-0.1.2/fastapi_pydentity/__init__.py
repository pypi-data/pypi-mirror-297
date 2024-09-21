import inspect
from collections.abc import Iterable, Callable
from typing import Annotated

from fastapi import Depends
from pydenticore import (
    DefaultUserConfirmation,
    IdentityConstants,
    IdentityErrorDescriber,
    IdentityOptions,
    RoleManager,
    SignInManager,
    UpperLookupNormalizer,
    UserClaimsPrincipalFactory,
    UserManager,
)
from pydenticore.authentication import AuthenticationOptions, AuthenticationSchemeProvider
from pydenticore.authentication.interfaces import IAuthenticationSchemeProvider, IAuthenticationOptionsAccessor
from pydenticore.authorization import (
    AuthorizationOptions,
    AuthorizationPolicy,
    AuthorizationPolicyProvider,
)
from pydenticore.authorization.interfaces import IAuthorizationOptionsAccessor, IAuthorizationPolicyProvider
from pydenticore.hashers import Argon2PasswordHasher
from pydenticore.http.context import IHttpContextAccessor
from pydenticore.interfaces import (
    ILogger,
    ILookupNormalizer,
    IPasswordHasher,
    IPasswordValidator,
    IRoleValidator,
    IUserClaimsPrincipalFactory,
    IUserConfirmation,
    IUserValidator,
)
from pydenticore.interfaces.stores import IUserStore, IRoleStore
from pydenticore.types import TUser, TRole
from pydenticore.validators import UserValidator, RoleValidator, PasswordValidator

from fastapi_pydentity.authentication import AuthenticationBuilder, AuthenticationMiddleware
from fastapi_pydentity.authorization import AuthorizationBuilder
from fastapi_pydentity.dependencies import (
    AuthenticationOptionsAccessor,
    AuthorizationHandlerContext,
    AuthorizationOptionsAccessor,
    BaseAuthorizationHandlerContext,
    BaseHttpContext,
    HttpContext,
    HttpContextAccessor,
)
from fastapi_pydentity.identity import IdentityBuilder
from fastapi_pydentity.infrastructure import ServiceCollection, IterableDependency, services


class PydentityBuilder:
    def __init__(self):
        self.services = services

    def add_authentication(self, default_scheme: str | None = None) -> AuthenticationBuilder:
        """
        Registers services required by authentication services.

        :param default_scheme:
        :return:
        """
        self.services.add_singleton(AuthenticationOptions)
        self.services.add_scoped(BaseHttpContext, HttpContext)
        self.services.add_scoped(IHttpContextAccessor, HttpContextAccessor)
        self.services.add_scoped(IAuthenticationOptionsAccessor, AuthenticationOptionsAccessor)
        self.services.add_scoped(IAuthenticationSchemeProvider, AuthenticationSchemeProvider)

        options = self.services.get(AuthenticationOptions)()
        options.default_authentication_scheme = IdentityConstants.ApplicationScheme
        options.default_sign_in_scheme = IdentityConstants.ExternalScheme

        if default_scheme:
            options.default_scheme = default_scheme
            options.default_authentication_scheme = ""

        return AuthenticationBuilder(options)

    def add_authorization(self, default_policy: AuthorizationPolicy | None = None) -> AuthorizationBuilder:
        """
         Adds authorization policy services.

        :param default_policy:
        :return:
        """
        self.services.add_singleton(AuthorizationOptions)
        self.services.add_scoped(IAuthorizationOptionsAccessor, AuthorizationOptionsAccessor)
        self.services.add_scoped(IAuthorizationPolicyProvider, AuthorizationPolicyProvider)
        self.services.add_scoped(BaseAuthorizationHandlerContext, AuthorizationHandlerContext)

        options = self.services.get(AuthorizationOptions)()

        if default_policy:
            options.default_policy = default_policy

        return AuthorizationBuilder(options)

    def add_identity(
            self,
            user_store: type[IUserStore],
            role_store: type[IRoleStore],
            configure: Callable[[IdentityOptions], None] | None = None
    ) -> IdentityBuilder:
        """
        Adds and configures the identity system for the specified User and Role types.

        :param user_store: The type representing a User in the system.
        :param role_store: The type representing a Role in the system.
        :param configure: An action to configure the ``IdentityOptions``.
        :return:
        """
        self.add_authentication().add_identity_cookies()

        validator_signature = inspect.Signature(
            parameters=[
                inspect.Parameter(
                    "errors",
                    annotation=Annotated[IdentityErrorDescriber, Depends()],
                    kind=inspect.Parameter.POSITIONAL_OR_KEYWORD
                ),
            ],
        )

        password_validators = IterableDependency()
        password_validators.__signature__ = validator_signature

        user_validators = IterableDependency()
        user_validators.__signature__ = validator_signature

        role_validators = IterableDependency()
        role_validators.__signature__ = validator_signature

        self.services.add_singleton(IdentityOptions)
        self.services.add_scoped(ILogger["UserManager"], lambda: None)
        self.services.add_scoped(ILogger["RoleManager"], lambda: None)
        self.services.add_scoped(ILogger["SignInManager"], lambda: None)
        self.services.add_scoped(IUserStore[TUser], user_store)
        self.services.add_scoped(IRoleStore[TRole], role_store)
        self.services.add_scoped(IdentityErrorDescriber, IdentityErrorDescriber)
        self.services.add_scoped(IPasswordHasher[TUser], Argon2PasswordHasher)
        self.services.add_scoped(ILookupNormalizer, UpperLookupNormalizer)
        self.services.add_scoped(Iterable[IPasswordValidator[TUser]], password_validators)
        self.services.add_scoped(Iterable[IUserValidator[TUser]], user_validators)
        self.services.add_scoped(Iterable[IRoleValidator[TRole]], role_validators)
        self.services.add_scoped(UserManager[TUser], UserManager)
        self.services.add_scoped(RoleManager[TRole], RoleManager)
        self.services.add_scoped(IUserConfirmation[TUser], DefaultUserConfirmation)
        self.services.add_scoped(IUserClaimsPrincipalFactory[TUser], UserClaimsPrincipalFactory)
        self.services.add_scoped(SignInManager[TUser], SignInManager)

        if configure:
            configure(self.services.get(IdentityOptions)())

        return IdentityBuilder(self.services)

    def add_default_identity(
            self,
            user_store: type[IUserStore],
            role_store: type[IRoleStore],
    ) -> IdentityBuilder:
        """
        Adds a set of common identity services to the application, token providers,
        and configures authentication to use identity cookies.

        :param user_store: The type representing a IUserStore in the system.
        :param role_store: The type representing a IRoleStore in the system.
        :return:
        """
        builder = self.add_identity(user_store, role_store)
        builder.add_default_token_providers()
        self.services.get(Iterable[IPasswordValidator[TUser]]).add(PasswordValidator)
        self.services.get(Iterable[IUserValidator[TUser]]).add(UserValidator)
        self.services.get(Iterable[IRoleValidator[TRole]]).add(RoleValidator)
        return builder

    def build(self):
        self.services.build()
