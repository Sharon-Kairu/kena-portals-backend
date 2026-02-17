from django.db import models
from users.models import User
from courses.models import Course,CourseCategory

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
    category = models.ForeignKey(
    CourseCategory, 
        on_delete=models.CASCADE, 
        related_name='instructor_category',
        null=True,
        blank=True
    ) 
    instructor_id = models.CharField(max_length=15, unique=True, editable=False, blank=True)
    license_number = models.CharField(max_length=20, blank=True, null=True)  # For driving instructors
    date_of_birth = models.DateField()

    # ================= NEXT OF KIN =================
    nok_first_name = models.CharField(max_length=50)
    nok_last_name = models.CharField(max_length=50)
    nok_email = models.EmailField(blank=True)
    nok_phone = models.CharField(max_length=20)
    nok_relationship = models.CharField(max_length=50)
    nok_occupation = models.CharField(max_length=50, blank=True)
    def save(self, *args, **kwargs):
        if not self.instructor_id:
            last_instructor = Instructor.objects.order_by('-id').first()
            if last_instructor and last_instructor.instructor_id:
                last_number = int(last_instructor.instructor_id.replace('INS', ''))
                new_number = last_number + 1
            else:
                new_number = 1

            self.instructor_id = f"INS{new_number:04d}"

        super().save(*args, **kwargs)
    def __str__(self):
        return self.user.get_full_name()  # Display instructor’s name
