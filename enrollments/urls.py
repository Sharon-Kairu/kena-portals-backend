from django.urls import path,include
from enrollments.views import enroll_student

urlpatterns = [
    path('enroll', enroll_student, name='enroll-student'),
]