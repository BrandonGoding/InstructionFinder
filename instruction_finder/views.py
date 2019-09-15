from django.views import View
from instruction_finder.mixins import AuthenticationMixin
from django.http import JsonResponse

from instruction_finder.models import Course


class SessionViewSet(AuthenticationMixin, View):
    def get(self, request, *args, **kwargs):
        # Serialize objects
        # sessions = Session.objects.all().order_by('-session_date')[:20]
        # return JsonResponse(json.loads(sessions.to_json()), status=200, safe=False)
        return JsonResponse({"ok": "ok"}, status=200, safe=False)


class CourseAttributesFormView(AuthenticationMixin, View):

    def get(self, request, *args, **kwargs):
        """
        Get the course attributes in a JSON

        endpoint: GET - courses/14/attributes

        output:
        {
          "id": 14,
          "instructor": "Instructor Paul",
          "attributes": {
            "_id": "5d7ea56ca15775f2fb4dd475",
            "course_id": 14,
            "course_title": "Mongo Course",
            "is_active": false,
            "course_description": "This is a Mongo Course",
            "tags": ["tech"],
            "custom": []
          }
        }

        """
        if "pk" in kwargs:
            course = None

            # Find the course
            try:
                course = Course.objects.get(pk=kwargs["pk"])
            except (TypeError, ValueError, OverflowError, Course.DoesNotExist):
                return JsonResponse({"error": "Course not found."}, status=401)

            # Get the course attributes
            try:
                attributes = course.get_course_attributes_object()
            except KeyError:
                return JsonResponse({"error": "Course attributes not found."},
                                    status=404)

            attributes_data = attributes.to_mongo().to_dict()
            attributes_data["_id"] = str(attributes.id)

            data = {
                "id": course.id,
                "instructor": str(course.instructor),
                'attributes': attributes_data
            }

            return JsonResponse(data, status=200)

        return JsonResponse({"error": "Invalid course ID."}, status=401)

        def put(self, request, *args, **kwargs):

            """
            Update course attributes
            """
            pass
