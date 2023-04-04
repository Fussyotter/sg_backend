import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        async def inner():
            # Get the token from the request header
            token = request.META.get('HTTP_AUTHORIZATION')

            # Authenticate the user using the token
            if token:
                # Verify the token
                try:
                    decoded_token = jwt.decode(token, settings.SECRET_KEY)
                    user_id = decoded_token.get('user_id')
                    user = User.objects.get(id=user_id)
                    request.user = user
                except (jwt.DecodeError, User.DoesNotExist):
                    raise PermissionDenied('Invalid token')

            response = await self.get_response(request)
            return response

        return inner()
