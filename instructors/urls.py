from django.urls import path,include
from . import views

urlpatterns = [
    path('register/', views.RegisterInstructorView.as_view(), name='instructor-register'),
    path('get_instructors/',views.GetInstructors.as_view(), name='get-instructors')
]
