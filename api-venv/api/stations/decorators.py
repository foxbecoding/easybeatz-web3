from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def check_user_pubkey(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        user_pubkey = str(kwargs.get("pk"))
        if str(request.user) != user_pubkey:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(self, request, *args, **kwargs)
    return wrapper
