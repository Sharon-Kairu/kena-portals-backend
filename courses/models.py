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
    
class CourseCategory(models.Model):
    """Subcategories within a course (e.g., Practical/Theory for Driving)"""
    
    CATEGORY_CHOICES = (
        ('practical', 'Practical'),
        ('theory', 'Theory'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name_plural = "Course Categories"
        ordering = ['order']
        unique_together = ['course', 'name']
    
    def __str__(self):
        return f"{self.course.name} - {self.get_name_display()}"

class Module(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    category = models.ForeignKey(
        CourseCategory, 
        on_delete=models.CASCADE, 
        related_name='modules',
        null=True,
        blank=True
    ) 
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
