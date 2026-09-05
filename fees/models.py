from django.db import models
from students.models import Student


class Fee(models.Model):

    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Partial", "Partial"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    receipt_no = models.CharField(
        max_length=30,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    due_date = models.DateField()

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    remarks = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.receipt_no} - {self.student.first_name}"
