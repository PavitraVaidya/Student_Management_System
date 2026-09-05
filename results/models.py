from django.db import models
from students.models import Student
from exams.models import Exam


class Result(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    marks = models.PositiveIntegerField()

    grade = models.CharField(
        max_length=5,
        blank=True
    )

    result = models.CharField(
        max_length=10,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.marks >= 90:
            self.grade = "A+"
        elif self.marks >= 80:
            self.grade = "A"
        elif self.marks >= 70:
            self.grade = "B"
        elif self.marks >= 60:
            self.grade = "C"
        elif self.marks >= 50:
            self.grade = "D"
        else:
            self.grade = "F"

        if self.marks >= self.exam.passing_marks:
            self.result = "Pass"
        else:
            self.result = "Fail"

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("student", "exam")

    def __str__(self):
        return f"{self.student.first_name} - {self.exam.exam_name}"
