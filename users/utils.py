"""
Module for user tools definition.
"""
from datetime import datetime, timedelta
from functools import wraps
from datetime import datetime
import graphql_jwt
from django.contrib.auth.models import User



# A principio so funciona se o token vier na forma:
# "Authorization": "JWT token""
# TODO implementar uma alterantiva para receber Bearer token
def access_required(function):
    """
    Verify if the user is logged on the system.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        user_token = args[1].context.META.get('HTTP_AUTHORIZATION')

        try:
            kind, token = user_token.split()
        except:
            raise Exception('Invalid authorization data!')

        if kind.lower() != 'jwt':
            raise Exception('Invalid authorization method!')

        validator = graphql_jwt.Verify.Field()
        payload = validator.resolver(None, args[1], token).payload
        username = payload.get('username')
        expiration_time = payload.get('exp', 0)
        now = datetime.now() - timedelta(hours=3)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception('Invalid validation data!')

        if (now.timestamp() > expiration_time):
            raise Exception('Session expired')

        if user.is_anonymous:
            raise Exception('Not logged in!')

        kwargs['user'] = user
        return function(*args, **kwargs)
    return decorated
