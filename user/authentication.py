from django.conf import settings
from rest_framework import authentication
import jwt
from rest_framework import exceptions
from . import models
"""
here we are going to write our custom authentication
"""


class CustomAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")
        user = models.User.objects.filter(id=payload['id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")
        return (user, None)