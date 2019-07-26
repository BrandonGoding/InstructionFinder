from django.views import View
# from instruction_finder.mongo_models import Session, Seat
import random
import datetime
from instruction_finder.models import Course, User, Profile
import json
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import JsonResponse


class SessionViewSet(View):

    def get(self, request, *args, **kwargs):
        # Get auth Class
        auth = JSONWebTokenAuthentication()

        # Try to authenticate
        try:
            authentication = auth.authenticate(request)
            print(authentication)

        except AuthenticationFailed as e:
            return JsonResponse({
                "error": str(e)
            }, status=401)

        # I token was not found
        if authentication is None:
            return JsonResponse({
                "error": "Token has not been provided"
            }, status=401)

        # Serialize objects
        # sessions = Session.objects.all().order_by('-session_date')[:20]
        # return JsonResponse(json.loads(sessions.to_json()), status=200, safe=False)
        return JsonResponse({"ok": "ok"}, status=200, safe=False)
