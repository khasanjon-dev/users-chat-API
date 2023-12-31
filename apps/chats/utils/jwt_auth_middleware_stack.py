import traceback

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode, InvalidSignatureError, ExpiredSignatureError, DecodeError

from root import settings
from users.models import User


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            if jwt_token_list := scope.get('query_string'):
                jwt_token_list = jwt_token_list.decode('utf8')
                jwt_token = str(jwt_token_list).split('auth=')[-1]
                jwt_payload = self.get_payload(jwt_token)
                user_credentials = self.get_user_credentials(jwt_payload)
                user = await self.get_logged_in_user(user_credentials)
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()
        except (InvalidSignatureError, KeyError, ExpiredSignatureError, DecodeError):
            traceback.print_exc()
        except Exception:
            scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)

    def get_payload(self, jwt_token):
        payload = jwt_decode(jwt_token, settings.SECRET_KEY, ['HS256'])
        return payload

    def get_user_credentials(self, payload):
        '''
        method to get user credentials from jwt token payload.
        defaults to user id.
        '''
        user_id = payload['user_id']
        return user_id

    async def get_logged_in_user(self, user_id):
        user = await self.get_user(user_id)
        return user

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
