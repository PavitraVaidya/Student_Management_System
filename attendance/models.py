from django.db import models
from students.models import Student
from courses.models import Subject
from teachers.models import Teacher


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
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

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    remarks = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        unique_together = ('student', 'subject', 'date')

    def __str__(self):
        return f"{self.enrollment.student.first_name} - {self.date}"

