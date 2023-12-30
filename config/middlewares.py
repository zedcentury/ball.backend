from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Extract token from query parameters or headers
        # print(scope)
        token = scope.get('query_string').decode('utf-8').split('=')[1]
        print(token)
        if not token:
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        # Authenticate the user based on the token
        user = await self.get_user_from_token(token)
        if user is None:
            scope[user] = AnonymousUser()
        else:
            scope['user'] = user

        # Continue with the middleware chain
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            return Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return None
