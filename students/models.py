from django.db import models
from django.conf import settings
from courses.models import Course


class Student(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    admission_no = models.CharField(max_length=20, unique=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    dob = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    parent_name = models.CharField(max_length=100)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    admission_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(
    upload_to="students/",
    blank=True,
    null=True
)

    def __str__(self):
        return f"{self.admission_no} - {self.first_name} {self.last_name}"
class Enrollment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    semester = models.PositiveIntegerField()

    academic_year = models.CharField(max_length=20)

    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Dropped', 'Dropped'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    def __str__(self):
        return f"{self.student.first_name} - {self.course.course_name}"