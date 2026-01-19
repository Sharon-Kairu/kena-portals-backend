from django.db import models
from users.models import User
from courses.models import Course

class Instructor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category= models.ForeignKey(Course, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=15, unique=True)
    instructor_id = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()

    # ================= NEXT OF KIN =================
    nok_first_name = models.CharField(max_length=50)
    nok_last_name = models.CharField(max_length=50)
    nok_email = models.EmailField(blank=True)
    nok_phone = models.CharField(max_length=20)
    nok_relationship = models.CharField(max_length=50)
    nok_occupation = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.get_full_name()  # Display instructor’s name
