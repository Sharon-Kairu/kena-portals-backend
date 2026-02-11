from django.db import models
from students.models import Student
from courses.models import Course

class Request(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('approved','Approved'),
        ('denied','Denied'),
    ]
    student=models.ForeignKey("students.Student", on_delete=models.CASCADE)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date_posted=models.DateField()
    request_date=models.DateField()
    request_time=models.TimeField()
    request_reason=models.TextField(max_length=50)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES)
   
