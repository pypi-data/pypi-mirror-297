from collections.abc import Callable, Iterable
from typing import Annotated, overload, Any

from fastapi import Depends, FastAPI
from pydenticore.authorization import (
    AuthorizationError,
    AuthorizationOptions,
    AuthorizationPolicy,
    AuthorizationPolicyBuilder,
    AuthorizationPolicyProvider,
)
from pydenticore.authorization.interfaces import IAuthorizationPolicyProvider
from pydenticore.exc import InvalidOperationException
from starlette.responses import PlainTextResponse
from starlette.types import ExceptionHandler

from fastapi_pydentity.dependencies import AuthorizationHandlerContext, BaseAuthorizationHandlerContext


def use_authorization(app: FastAPI, on_error: ExceptionHandler | None = None):
    if on_error:
        app.add_exception_handler(AuthorizationError, on_error)
    else:
        app.add_exception_handler(
            AuthorizationError,
            lambda req, exc: PlainTextResponse("Forbidden", status_code=403)
        )


def Authorize(roles: str | Iterable[str] | None = None, policy: str | None = None) -> Any:
    """
    Indicates that the route or router to which this dependency is applied requires the specified authorization.

    :param roles: A list of roles that are allowed to access the resource.
    :param policy: Policy name that determines access to the resource.
    :return:
    """

    async def decorator(
            context: Annotated[BaseAuthorizationHandlerContext, Depends(AuthorizationHandlerContext)],
            provider: Annotated[IAuthorizationPolicyProvider, Depends(AuthorizationPolicyProvider)],
    ):
        if not context.user:
            raise AuthorizationError()  # TODO: or AuthenticationError?

        await _check_roles(roles, context)
        await _check_policy(policy, context, provider)

    return Depends(decorator)


async def _check_roles(roles: str | Iterable[str] | None, context: BaseAuthorizationHandlerContext) -> None:
    if roles:
        if isinstance(roles, str):
            roles = set(roles.replace(" ", "").split(","))
        else:
            roles = set(roles)

        result = any([context.user.is_in_role(r) for r in roles])

        if not result:
            raise AuthorizationError()


async def _check_policy(
        policy: str | None,
        context: BaseAuthorizationHandlerContext,
        provider: IAuthorizationPolicyProvider
) -> None:
    if policy:
        _policy = await provider.get_policy(policy)

        if not _policy:
            raise InvalidOperationException(f"The AuthorizationPolicy named: '{policy}' was not found.")

        for req in _policy.requirements:
            await req.handle(context)

        if not context.has_succeeded:
            raise AuthorizationError()
    else:
        if default_policy := await provider.get_default_policy():
            for req in default_policy.requirements:
                await req.handle(context)


class AuthorizationBuilder:
    """Used to configure authorization."""

    __slots__ = ("_options",)

    def __init__(self, options: AuthorizationOptions):
        self._options = options

    @overload
    def add_policy(self, name: str, policy: AuthorizationPolicy) -> "AuthorizationBuilder":
        """
        Adds a ``AuthorizationPolicy``.

        :param name: The name of this policy.
        :param policy: The ``AuthorizationPolicy``.
        :return:
        """

    @overload
    def add_policy(
            self,
            name: str,
            configure_policy: Callable[[AuthorizationPolicyBuilder], None]
    ) -> "AuthorizationBuilder":
        """
        Add a policy that is built from a delegate with the provided name.

        :param name: The name of the policy.
        :param configure_policy: The delegate that will be used to build the policy.
        :return:
        """

    def add_policy(
            self,
            name: str,
            policy_or_builder: AuthorizationPolicy | Callable[[AuthorizationPolicyBuilder], None]
    ) -> "AuthorizationBuilder":
        self._options.add_policy(name, policy_or_builder)
        return self

    def __iadd__(self, other: AuthorizationPolicy):
        return self.add_policy(other.name, other)
