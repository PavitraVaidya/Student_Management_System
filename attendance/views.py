from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Attendance
from .forms import AttendanceForm


# -----------------------------
# Attendance List
# -----------------------------
def attendance_list(request):

    attendance = Attendance.objects.select_related(
        "student",
        "subject",
        "teacher"
    ).all().order_by("-date")

    search = request.GET.get("search")

    if search:
        attendance = attendance.filter(
    Q(student__first_name__icontains=search) |
    Q(student__last_name__icontains=search) |
    Q(subject__subject_name__icontains=search)
)

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendance": attendance
        }
    )


# -----------------------------
# Add Attendance
# -----------------------------
def add_attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance Added Successfully."
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


# -----------------------------
# Edit Attendance
# -----------------------------
def edit_attendance(request, pk):

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
                "Attendance Updated Successfully."
            )

            return redirect("attendance_list")

    else:

        form = AttendanceForm(instance=attendance)

    return render(
        request,
        "attendance/attendance_form.html",
        {
            "form": form,
            "title": "Edit Attendance"
        }
    )


# -----------------------------
# Delete Attendance
# -----------------------------
def delete_attendance(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    attendance.delete()

    messages.success(
        request,
        "Attendance Deleted Successfully."
    )

    return redirect("attendance_list")


# -----------------------------
# Attendance Details
# -----------------------------
def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance
        }
    )
