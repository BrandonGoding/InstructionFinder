from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse


class AuthenticationMixin:
    """
    Authentication class to validate API JWT token in the header
    """

    def dispatch(self, *args, **kwargs):

        # Get auth Class
        auth = JSONWebTokenAuthentication()

        # Try to authenticate the params in request
        try:
            authentication = auth.authenticate(self.request)

        except AuthenticationFailed as e:
            return JsonResponse({"error": str(e)}, status=401)

        # If token was not found
        if authentication is None:
            return JsonResponse({"error": "Token has not been provided"}, status=401)

        return super().dispatch(*args, **kwargs)
