from django.db import models

# Create your models here.
class Course(models.Model):
    COURSE_CHOICES=(
        ('driving', 'Driving'),
        ('computer', 'Computer'),
        ('ai', 'AI'),
    )

    name=models.CharField(max_length=20, choices=COURSE_CHOICES)
    def __str__(self):
        return self.name


class Module(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title=models.CharField(max_length=100)
    order=models.PositiveIntegerField(default=1)

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('bronze', 'Bronze'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    included_courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name
