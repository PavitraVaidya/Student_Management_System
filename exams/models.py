from django.db import models
from courses.models import Subject


class Exam(models.Model):

    exam_name = models.CharField(max_length=100)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    exam_date = models.DateField()

    total_marks = models.PositiveIntegerField()

    passing_marks = models.PositiveIntegerField()

    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.exam_name} - {self.subject.subject_name}"
