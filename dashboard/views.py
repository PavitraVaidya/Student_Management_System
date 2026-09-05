from django.shortcuts import render

from students.models import Student
from teachers.models import Teacher
from courses.models import Course, Subject
from attendance.models import Attendance
from fees.models import Fee
from exams.models import Exam


def dashboard(request):

    recent_students = Student.objects.select_related(
        "course"
    ).order_by("-id")[:5]

    context = {
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "total_courses": Course.objects.count(),
        "total_subjects": Subject.objects.count(),
        "total_attendance": Attendance.objects.count(),
        "pending_fees": Fee.objects.filter(
            status="Pending"
        ).count(),
        "total_exams": Exam.objects.count(),

        "recent_students": recent_students,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )