from fastapi.requests import Request
from fastapi.responses import Response
from pydenticore.authentication import AuthenticationOptions
from pydenticore.authentication.interfaces import IAuthenticationSchemeProvider, IAuthenticationOptionsAccessor
from pydenticore.authorization import (
    AuthorizationHandlerContext as BaseAuthorizationHandlerContext,
    AuthorizationOptions,
)
from pydenticore.authorization.interfaces import IAuthorizationOptionsAccessor
from pydenticore.http.context import IHttpContextAccessor, HttpContext as BaseHttpContext
from pydenticore.security.claims import ClaimsPrincipal


class AuthenticationOptionsAccessor(IAuthenticationOptionsAccessor):
    def __init__(self, options: AuthenticationOptions):
        super().__init__(options)


class AuthorizationOptionsAccessor(IAuthorizationOptionsAccessor):
    def __init__(self, options: AuthorizationOptions):
        super().__init__(options)


class HttpContext(BaseHttpContext):
    def __init__(
            self,
            request: Request,
            response: Response,
            schemes: IAuthenticationSchemeProvider
    ):
        super().__init__(request, response, schemes)

    def _getuser(self) -> ClaimsPrincipal | None:
        return self.request.user

    def _setuser(self, value: ClaimsPrincipal | None) -> None:
        self.request.scope["user"] = value


class HttpContextAccessor(IHttpContextAccessor):
    def __init__(self, context: BaseHttpContext):
        super().__init__(context)


class AuthorizationHandlerContext(BaseAuthorizationHandlerContext):
    def __init__(self, request: Request):
        super().__init__(request)
