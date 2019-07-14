from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from instruction_finder.api.serializers import CourseSerializer
from instruction_finder.models import Course


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    #permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = Course.objects.all()

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        print(self.args)
        return super().dispatch(request, *args, **kwargs)