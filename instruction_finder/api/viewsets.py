from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from instruction_finder.api.serializers import CourseSerializer
from instruction_finder.models import Course


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Course.objects.all()
