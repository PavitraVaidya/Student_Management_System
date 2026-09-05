from django.db import models
from django.conf import settings
from courses.models import Subject


class Teacher(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    teacher_id = models.CharField(max_length=20, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    qualification = models.CharField(max_length=100)

    experience = models.PositiveIntegerField(help_text="Years of experience")

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.teacher_id} - {self.first_name} {self.last_name}"
