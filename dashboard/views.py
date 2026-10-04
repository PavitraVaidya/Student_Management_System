from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from students.models import Student
from teachers.models import Teacher
from courses.models import Course, Subject
from attendance.models import Attendance
from fees.models import Fee
from exams.models import Exam
from assignments.models import Assignment
from results.models import Result


@login_required
def dashboard(request):

    user = request.user

    

    if user.role == "ADMIN":

        recent_students = (
            Student.objects
            .select_related("course")
            .order_by("-id")[:5]
        )

        context = {
            "role": "ADMIN",

            "total_students": Student.objects.count(),
            "total_teachers": Teacher.objects.count(),
            "total_courses": Course.objects.count(),
            "total_subjects": Subject.objects.count(),

            "total_attendance": Attendance.objects.count(),

            "pending_fees": Fee.objects.filter(
                status="Pending"
            ).count(),

            "total_exams": Exam.objects.count(),

            "total_assignments": Assignment.objects.count(),

            "total_results": Result.objects.count(),

            "recent_students": recent_students,
        }




    elif user.role == "TEACHER":

        teacher = (
            Teacher.objects
            .select_related(
                "subject",
                "user"
            )
            .filter(user=user)
            .first()
        )

        recent_students = (
            Student.objects
            .select_related("course")
            .order_by("-id")[:5]
        )

        context = {
            "role": "TEACHER",

            "teacher": teacher,

            "total_students": Student.objects.count(),

            "total_courses": Course.objects.count(),

            "total_subjects": Subject.objects.count(),

            "total_attendance": Attendance.objects.count(),

            "total_exams": Exam.objects.count(),

            "total_assignments": Assignment.objects.count(),

            "total_results": Result.objects.count(),

            "recent_students": recent_students,
        }


    # =====================================================
    # STUDENT DASHBOARD
    # =====================================================

    elif user.role == "STUDENT":

        student = (
            Student.objects
            .select_related(
                "course",
                "user"
            )
            .filter(user=user)
            .first()
        )

     
        if student is None:

            context = {
                "role": "STUDENT",
                "student": None,
            }

            return render(
                request,
                "dashboard/dashboard.html",
                context
            )




        attendance = Attendance.objects.filter(
            student=student
        )

        total_attendance = attendance.count()

        present_count = attendance.filter(
            status="Present"
        ).count()

        absent_count = attendance.filter(
            status="Absent"
        ).count()

        late_count = attendance.filter(
            status="Late"
        ).count()


        # -------------------------------------------------
        # ATTENDANCE PERCENTAGE
        # -------------------------------------------------

        if total_attendance > 0:

            attendance_percentage = round(
                (
                    present_count /
                    total_attendance
                ) * 100,
                2
            )

        else:

            attendance_percentage = 0


  

        fees = Fee.objects.filter(
            student=student
        )

        pending_fees = fees.filter(
            status="Pending"
        ).count()

        paid_fees = fees.filter(
            status="Paid"
        ).count()

        partial_fees = fees.filter(
            status="Partial"
        ).count()


        

        assignments = Assignment.objects.filter(
            student=student
        )

        total_assignments = assignments.count()

        pending_assignments = assignments.filter(
            status="Pending"
        ).count()

        submitted_assignments = assignments.filter(
            status="Submitted"
        ).count()


       

        results = (
            Result.objects
            .filter(student=student)
            .select_related(
                "exam",
                "exam__subject"
            )
            .order_by("-id")
        )

        total_results = results.count()


       

        exams = (
            Exam.objects
            .filter(
                subject__course=student.course
            )
            .select_related("subject")
            .order_by("exam_date")
        )

        total_exams = exams.count()


        context = {

            "role": "STUDENT",

            "student": student,

            # Attendance
            "total_attendance": total_attendance,
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "attendance_percentage": attendance_percentage,

            # Fees
            "pending_fees": pending_fees,
            "paid_fees": paid_fees,
            "partial_fees": partial_fees,

            # Assignments
            "total_assignments": total_assignments,
            "pending_assignments": pending_assignments,
            "submitted_assignments": submitted_assignments,

            # Results
            "total_results": total_results,

            # Exams
            "total_exams": total_exams,

            # Lists
            "recent_results": results[:5],
            "upcoming_exams": exams[:5],
        }


 

    else:

        context = {
            "role": "UNKNOWN"
        }


    return render(
        request,
        "dashboard/dashboard.html",
        context
    )