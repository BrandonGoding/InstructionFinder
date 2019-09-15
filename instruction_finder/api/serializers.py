from rest_framework.serializers import ModelSerializer

from instruction_finder.models import Course, Instructor


class InstructorSerializer(ModelSerializer):
    class Meta:
        model = Instructor
        fields = ("id", "user")


class CourseSerializer(ModelSerializer):
    instructor = InstructorSerializer(many=False)

    class Meta:
        model = Course
        fields = ("id", "instructor", "title", "description", "is_active")
