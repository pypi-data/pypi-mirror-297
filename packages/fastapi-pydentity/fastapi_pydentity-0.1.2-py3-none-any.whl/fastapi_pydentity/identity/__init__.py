from collections.abc import Callable, Iterable

from pydenticore import (
    IdentityErrorDescriber,
    RoleManager,
    SignInManager,
    UserManager,
)
from pydenticore.identity_options import TokenOptions, IdentityOptions
from pydenticore.interfaces import (
    ILogger,
    IPasswordValidator,
    IRoleValidator,
    IUserClaimsPrincipalFactory,
    IUserConfirmation,
    IUserTwoFactorTokenProvider,
    IUserValidator,
)
from pydenticore.interfaces.stores import IUserStore, IRoleStore
from pydenticore.token_providers import (
    AuthenticatorTokenProvider,
    DataProtectorTokenProvider,
    EmailTokenProvider,
    PhoneNumberTokenProvider,
)
from pydenticore.types import TUser, TRole

from fastapi_pydentity.infrastructure import ServiceCollection


class IdentityBuilder:
    def __init__(self, services: ServiceCollection) -> None:
        self._services = services

    def add_user_validator(self, validator: type[IUserValidator[TUser]]) -> "IdentityBuilder":
        self._services.get(Iterable[IUserValidator[TUser]]).add(validator)
        return self

    def add_user_claims_principal_factory(self, factory: type[IUserClaimsPrincipalFactory[TUser]]) -> "IdentityBuilder":
        self._services.add_scoped(IUserClaimsPrincipalFactory[TUser], factory)
        return self

    def add_identity_error_describer(self, describer: type[IdentityErrorDescriber]) -> "IdentityBuilder":
        self._services.add_scoped(IdentityErrorDescriber, describer)
        return self

    def add_password_validator(self, validator: type[IPasswordValidator[TUser]]) -> "IdentityBuilder":
        self._services.get(Iterable[IPasswordValidator[TUser]]).add(validator)
        return self

    def add_user_store(self, store: type[IUserStore[TUser]]) -> "IdentityBuilder":
        self._services.add_scoped(IUserStore[TUser], store)
        return self

    def add_user_manager(self, manager: type[UserManager[TUser]]) -> "IdentityBuilder":
        self._services.add_scoped(UserManager[TUser], manager)
        return self

    def add_role_validator(self, validator: type[IRoleValidator[TRole]]) -> "IdentityBuilder":
        self._services.get(Iterable[IRoleValidator[TRole]]).add(validator)
        return self

    def add_role_store(self, store: type[IRoleStore[TRole]]) -> "IdentityBuilder":
        self._services.add_scoped(IRoleStore[TRole], store)
        return self

    def add_role_manager(self, manager: type[RoleManager[TRole]]) -> "IdentityBuilder":
        self._services.add_scoped(RoleManager[TRole], manager)
        return self

    def add_user_confirmation(self, user_confirmation: type[IUserConfirmation[TUser]]) -> "IdentityBuilder":
        self._services.add_scoped(IUserConfirmation[TUser], user_confirmation)
        return self

    def add_token_provider(self, provider_name: str, provider: IUserTwoFactorTokenProvider[TUser]) -> "IdentityBuilder":
        options = self._services.get(IdentityOptions)()
        options.tokens.provider_map[provider_name] = provider
        return self

    def add_signin_manager(self, manager: type[SignInManager[TUser]]) -> "IdentityBuilder":
        self._services.add_scoped(SignInManager[TUser], manager)
        return self

    def add_default_token_providers(self) -> "IdentityBuilder":
        self.add_token_provider(TokenOptions.DEFAULT_PROVIDER, DataProtectorTokenProvider())
        self.add_token_provider(TokenOptions.DEFAULT_EMAIL_PROVIDER, EmailTokenProvider())
        self.add_token_provider(TokenOptions.DEFAULT_PHONE_PROVIDER, PhoneNumberTokenProvider())
        self.add_token_provider(TokenOptions.DEFAULT_AUTHENTICATION_PROVIDER, AuthenticatorTokenProvider())
        return self

    def add_user_manager_logger(self, logger: ILogger[UserManager]) -> "IdentityBuilder":
        self._services.add_scoped(ILogger["UserManager"], logger)
        return self

    def add_role_manager_logger(self, logger: ILogger[RoleManager]) -> "IdentityBuilder":
        self._services.add_scoped(ILogger["RoleManager"], logger)
        return self

    def add_signin_manager_logger(self, logger: ILogger[SignInManager]) -> "IdentityBuilder":
        self._services.add_scoped(ILogger["SignInManager"], logger)
        return self

    def configure_options(self, configure: Callable[[IdentityOptions], None]) -> "IdentityBuilder":
        configure(self._services.get(IdentityOptions)())
        return self
