from django.urls import path, include
from .views import (
    AllStudentsView, 
    MeStudentView, 
    IndividualStudentView,
    StudentModulesView,
    InstructorStudentModulesView,
    GradeModuleView
)

urlpatterns = [
    path('me/', MeStudentView.as_view(), name='me-student'),
    path('all_students/', AllStudentsView.as_view(), name='all-students'),
    path('my-modules/', StudentModulesView.as_view(), name='student-modules'),
    path('<str:student_id>/', IndividualStudentView.as_view(), name='individual-student'),
]
