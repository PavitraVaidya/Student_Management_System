from django.db import models
from students.models import Student
from courses.models import Subject
from teachers.models import Teacher


class Assignment(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Submitted", "Submitted"),
        ("Late", "Late"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    due_date = models.DateField()

    submission_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.title} - {self.student.first_name}"