from django.db import models
from users.models import User
from courses.models import Course, SubscriptionPlan

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )
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
    driving_pdl= models.CharField(null=True, blank=True, unique=True, max_length=20)

    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.order_by('-id').first()
            if last_student and last_student.student_id:
                last_number = int(last_student.student_id.replace('STD', ''))
                new_number = last_number + 1
            else:
                new_number = 1

            self.student_id = f"STD{new_number:04d}"

        super().save(*args, **kwargs)


class StudentModule(models.Model):
    COMMENT_OPTIONS=(
        ('excellent', 'Excellent'),
        ('good','Good'),
        ('fair', 'Fair')

    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='module_progress')
    module = models.ForeignKey('courses.Module', on_delete=models.CASCADE, related_name='student_progress')
    instructor = models.ForeignKey('instructors.Instructor', on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_modules')
    status = models.CharField(
        max_length=20,
        choices=(('pending', 'Pending'), ('completed', 'Completed')),
        default='pending'
    )
    date_graded = models.DateField(null=True, blank=True)
    comment = models.CharField(blank=True, choices=COMMENT_OPTIONS, max_length=10)

    class Meta:
        unique_together = ('student', 'module')
        ordering = ['module__order']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.module.title}"
