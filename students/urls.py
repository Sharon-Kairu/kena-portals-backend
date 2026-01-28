from django.urls import path, include
from .views import AllStudentsView, MeStudentView,IndividualStudentView

urlpatterns = [
    path('me/', MeStudentView.as_view(), name='me-student'),
    path('all_students/', AllStudentsView.as_view(), name='all-students'),
    path('<str:student_id>/', IndividualStudentView.as_view(), name='individual-student'),
    
]
