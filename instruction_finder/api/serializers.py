from rest_framework.serializers import ModelSerializer

from instruction_finder.models import Course


class CourseSerializer(ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'instructor', 'title', 'description','is_active')

