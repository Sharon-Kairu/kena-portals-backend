from django.urls import path
from .views import CourseViewSet

urlpatterns = [
    path('', CourseViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', CourseViewSet.as_view({'get': 'retrieve'})),
]
