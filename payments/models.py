from django.db import models
from students.models import Student

class Payment(models.Model):
    PAYMENT_OPTIONS = (
        ('mpesa','Mpesa'),
        ('cash','Cash'),
        ('bank','Bank')
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_OPTIONS)
    transaction_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    receipt_number = models.CharField(max_length=20, unique=True, )

    def save(self, *args, **kwargs):
        if not self.receipt_number:  
            last_payment = Payment.objects.order_by('-id').first()
            if last_payment and last_payment.receipt_number:
                last_number = int(last_payment.receipt_number.replace('RCT', ''))
                new_number = last_number + 1
            else:
                new_number = 1

            self.receipt_number = f"RCT{new_number:04d}"  

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.amount} via {self.payment_method} ({self.receipt_number})"
