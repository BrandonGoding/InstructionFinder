from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from instruction_finder.api.viewsets import *
from instruction_finder.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # API
    path('obtain_token/', obtain_jwt_token),
    path('refresh_token/', refresh_jwt_token),

    path('courses/', CourseViewSet.as_view({'get': 'list',
                                            'post': 'create'})),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),

    # Mongo Models
    path('courses/<int:pk>/attributes', CourseAttributesFormView.as_view()),
]
