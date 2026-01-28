from django.db import models
from students.models import Student
from courses.models import Course,SubscriptionPlan

class Enrollment(models.Model):
    MODE_CHOICES=(
        ('standalone','Standalone'),
        ('subscription','Subscription')
    )
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    mode=models.CharField(max_length=20, choices=MODE_CHOICES)
    standalone_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name="standalone_students"
    )

    # Subscription
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    subscription_courses = models.ManyToManyField(
        Course,
        blank=True,
        related_name="subscription_students"
    )

    def clean(self):
        """
        Enforce business rules
        """
        if self.mode == 'standalone':
            if self.subscription_plan:
                raise ValidationError("Standalone cannot have subscription")

        if self.mode == 'subscription':
            if not self.subscription_plan:
                raise ValidationError("Subscription plan required")

            # Driving compulsory
            driving = Course.objects.get(code='driving')
            if driving not in self.subscription_courses.all():
                raise ValidationError("Driving is compulsory")
