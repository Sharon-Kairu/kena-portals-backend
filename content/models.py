from django.db import models
from courses.models import Course

class Content(models.Model):
    TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('audio', 'Audio'),
        ('video', 'Video')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='pdf')
    file = models.FileField(upload_to='course_content/')
    upload_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.course.name} - {self.title} ({self.type})"
