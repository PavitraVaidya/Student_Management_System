from django.db import models

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    duration = models.IntegerField(help_text="Duration in years")
    total_semesters = models.IntegerField(default=8)

    def __str__(self):
        return self.course_name
class Subject(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()

    def __str__(self):
        return self.subject_name
