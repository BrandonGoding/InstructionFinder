from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from instruction_finder.mongo_models import Course


class CourseView(View):
    def get(self, request, *args, **kwargs):
        course = Course()
        course.title = "Course A"
        course.description = "This is the description of Course A"
        course.instructor_id = 1
        course.save()
        return JsonResponse({"ok":"test", "course": course.to_json()}, status=200)