from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from instruction_finder.api.viewsets import *
from instruction_finder.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('obtain_token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),

    # path('test_create_course/', TestCourseView.as_view(), name='create_course'),

    # API
    path('courses/', CourseViewSet.as_view({'get': 'list'}), name='courses_list'),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'}), name='courses_create'),
    path('courses/', CourseViewSet.as_view({'post': 'create'}), name='courses_create'),

    # Mongo Models
    path('sessions/', SessionViewSet.as_view(), name='sessions_list')
]
