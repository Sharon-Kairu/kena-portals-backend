from django.urls import path,include
from . import views
from students.views import InstructorStudentModulesView, GradeModuleView

urlpatterns = [
    path('register/', views.RegisterInstructorView.as_view(), name='instructor-register'),
    path('get_instructors/',views.GetInstructors.as_view(), name='get-instructors'),
    path('students/',views.InstructorStudents.as_view(), name='instructor-students'),
    path('student-modules/', InstructorStudentModulesView.as_view(), name='instructor-student-modules'),
    path('grade-module/<int:module_id>/', GradeModuleView.as_view(), name='grade-module'),
]
