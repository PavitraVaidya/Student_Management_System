from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Attendance
from .forms import AttendanceForm
from students.models import Student


@login_required
def attendance_list(request):

    user = request.user

    if user.role in ["ADMIN", "TEACHER"]:

        attendance = (
            Attendance.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .all()
            .order_by("-date")
        )

        search = request.GET.get("search", "").strip()

        if search:

            attendance = attendance.filter(
                Q(student__first_name__icontains=search)
                |
                Q(student__last_name__icontains=search)
                |
                Q(subject__subject_name__icontains=search)
            )

    elif user.role == "STUDENT":

        try:

            student = Student.objects.get(
                user=user
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                "Your account is not linked to a student profile."
            )

            return redirect("dashboard")

        attendance = (
            Attendance.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .filter(
                student=student
            )
            .order_by("-date")
        )

        search = ""

    else:

        messages.error(
            request,
            "You do not have permission to view attendance."
        )

        return redirect("dashboard")

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendance": attendance,
            "search": search
        }
    )


@login_required
def add_attendance(request):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to add attendance."
        )

        return redirect("dashboard")

    if request.method == "POST":

        form = AttendanceForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance added successfully."
            )

            return redirect("attendance_list")

    else:

        form = AttendanceForm()

    return render(
        request,
        "attendance/attendance_form.html",
        {
            "form": form,
            "title": "Add Attendance"
        }
    )


@login_required
def edit_attendance(request, pk):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to edit attendance."
        )

        return redirect("dashboard")

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            instance=attendance
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance updated successfully."
            )

            return redirect("attendance_list")

    else:

        form = AttendanceForm(
            instance=attendance
        )

    return render(
        request,
        "attendance/attendance_form.html",
        {
            "form": form,
            "title": "Edit Attendance"
        }
    )


@login_required
def delete_attendance(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete attendance records."
        )

        return redirect("attendance_list")

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    if request.method == "POST":

        attendance.delete()

        messages.success(
            request,
            "Attendance deleted successfully."
        )

        return redirect("attendance_list")

    return render(
        request,
        "attendance/attendance_confirm_delete.html",
        {
            "attendance": attendance
        }
    )


@login_required
def attendance_detail(request, pk):

    user = request.user

    if user.role in ["ADMIN", "TEACHER"]:

        attendance = get_object_or_404(
            Attendance.objects.select_related(
                "student",
                "subject",
                "teacher"
            ),
            pk=pk
        )

    elif user.role == "STUDENT":

        try:

            student = Student.objects.get(
                user=user
            )

        except Student.DoesNotExist:

            messages.error(
                request,
                "Your account is not linked to a student profile."
            )

            return redirect("dashboard")

        attendance = get_object_or_404(
            Attendance.objects.select_related(
                "student",
                "subject",
                "teacher"
            ),
            pk=pk,
            student=student
        )

    else:

        messages.error(
            request,
            "You do not have permission to view attendance."
        )

        return redirect("dashboard")

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance
        }
    )