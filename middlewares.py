import base64
from aiohttp.web import middleware, Response

from settings import config

class LoginException(Exception):
    pass


@middleware
async def basic_auth_middleware(request, handler):
    try:
        auth = request.headers['Authorization']

        if not auth.startswith('Basic '):
            raise LoginException('Wrong authentication schema')
    
        user_password = auth[6:]
        user_password = base64.b64decode(user_password).decode()
        user, password = user_password.split(':')
        
        if not user == config['USER'] \
          or not password == config['PASSWORD']:
            raise LoginException('User creds are not provided correctly')

    except (LoginException, KeyError)  as e:
        return Response(
            status=401,
            text=str(e)
        )

    return await handler(request)
