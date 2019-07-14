from django.contrib import admin
from django.urls import path

from instruction_finder.views import TestCourseView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test_create_course/', TestCourseView.as_view(), name='create_course'),
]
