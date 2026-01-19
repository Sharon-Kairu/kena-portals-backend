from django.db import models
from users.models import User
from courses.models import Course, SubscriptionPlan

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # ================= COURSES / SUBSCRIPTION =================
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    # For standalone courses
    courses = models.ManyToManyField(Course, blank=True)

    # ================= NEXT OF KIN =================
    nok_first_name = models.CharField(max_length=50)
    nok_last_name = models.CharField(max_length=50)
    nok_email = models.EmailField(blank=True)
    nok_phone = models.CharField(max_length=20)
    nok_relationship = models.CharField(max_length=50)
    nok_occupation = models.CharField(max_length=50, blank=True)

    # ================= PAYMENT =================
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('paid', 'Paid'),
            ('partial', 'Partial'),
        ),
        default='pending'
    )
    driving_exam_date = models.DateField(null=True, blank=True)
    driving_pdl_date = models.DateField(null=True, blank=True)
    driving_pdl= models.CharField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.first_name


class StudentModule(models.Model):
    COMMENT_OPTIONS=(
        ('excellent', 'Excellent'),
        ('good','Good'),
        ('fair', 'Fair')

    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('completed', 'Completed')),
        default='pending'
    )
    date_graded = models.DateField(null=True, blank=True)
    comment = models.CharField(blank=True, options=COMMENT_OPTIONS)

    class Meta:
        unique_together = ('student', 'module')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.module.title}"
