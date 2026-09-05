from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from accounts.models import User
from .models import Teacher
from .forms import TeacherForm


# -----------------------------
# Teacher List
# -----------------------------
def teacher_list(request):

    teachers = Teacher.objects.select_related("subject").all().order_by("-id")

    search = request.GET.get("search")

    if search:
        teachers = teachers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(teacher_id__icontains=search) |
            Q(phone__icontains=search)
        )

    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": teachers
        }
    )


# -----------------------------
# Add Teacher
# -----------------------------
def add_teacher(request):

    if request.method == "POST":

        form = TeacherForm(request.POST)

        if form.is_valid():

            teacher = form.save(commit=False)

            username = teacher.teacher_id.lower()

            password = "Teacher@123"

            user = User.objects.create(

                username=username,

                email=teacher.email,

                password=make_password(password),

                role="TEACHER"

            )

            teacher.user = user

            teacher.save()

            messages.success(
                request,
                f"Teacher Added Successfully.\nUsername : {username}\nPassword : {password}"
            )

            return redirect("teacher_list")

    else:

        form = TeacherForm()

    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Add Teacher"
        }
    )


# -----------------------------
# Edit Teacher
# -----------------------------
def edit_teacher(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            instance=teacher
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Teacher Updated Successfully."
            )

            return redirect("teacher_list")

    else:

        form = TeacherForm(instance=teacher)

    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Edit Teacher"
        }
    )


# -----------------------------
# Delete Teacher
# -----------------------------
def delete_teacher(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    teacher.delete()

    messages.success(
        request,
        "Teacher Deleted Successfully."
    )

    return redirect("teacher_list")


# -----------------------------
# Teacher Details
# -----------------------------
def teacher_detail(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    return render(
        request,
        "teachers/teacher_detail.html",
        {
            "teacher": teacher
        }
    )
