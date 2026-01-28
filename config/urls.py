from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/instructors/', include('instructors.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/auth/', include('users.urls')),
    path('api/users/', include('users.urls')),
    path('api/enrollments/', include('enrollments.urls')),
    path('api/students/', include('students.urls')),
    path('api/payments/', include('payments.urls')),

]
