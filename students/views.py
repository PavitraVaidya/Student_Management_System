from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .models import Student
from .forms import StudentForm


@login_required
def student_list(request):

    if request.user.role not in ["ADMIN", "TEACHER"]:
        messages.error(
            request,
            "You do not have permission to view all students."
        )
        return redirect("dashboard")

    students = (
        Student.objects
        .select_related("course")
        .all()
        .order_by("-id")
    )

    search = request.GET.get("search", "").strip()

    if search:
        students = students.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(admission_no__icontains=search) |
            Q(phone__icontains=search)
        )

    paginator = Paginator(students, 10)

    page = request.GET.get("page")

    students = paginator.get_page(page)

    context = {
        "students": students,
        "search": search,
    }

    return render(
        request,
        "students/student_list.html",
        context
    )


@login_required
def add_student(request):

    if request.user.role not in ["ADMIN", "TEACHER"]:
        messages.error(
            request,
            "You do not have permission to add students."
        )
        return redirect("dashboard")

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            student = form.save(commit=False)

            username = student.admission_no.lower()

            password = "Student@123"

            if User.objects.filter(username=username).exists():

                messages.error(
                    request,
                    "A user with this admission number already exists."
                )

                return render(
                    request,
                    "students/student_form.html",
                    {
                        "form": form,
                        "title": "Add Student"
                    }
                )

            user = User.objects.create(
                username=username,
                email=student.email,
                password=make_password(password),
                role="STUDENT"
            )

            student.user = user

            student.save()

            messages.success(
                request,
                "Student added successfully. "
                f"Username: {username} | "
                f"Default Password: {password}"
            )

            return redirect("student_list")

    else:
        form = StudentForm()

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Add Student"
        }
    )


@login_required
def edit_student(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can edit student information."
        )

        return redirect("student_list")

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            updated_student = form.save()

            if updated_student.user:

                updated_student.user.email = updated_student.email

                updated_student.user.save()

            messages.success(
                request,
                "Student updated successfully."
            )

            return redirect("student_list")

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Edit Student"
        }
    )


@login_required
def delete_student(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete students."
        )

        return redirect("student_list")

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        user = student.user

        student.delete()

        if user:
            user.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect("student_list")

    return render(
        request,
        "students/student_confirm_delete.html",
        {
            "student": student
        }
    )


@login_required
def student_detail(request, pk):

    student = get_object_or_404(
        Student.objects.select_related(
            "course",
            "user"
        ),
        pk=pk
    )

    if request.user.role == "STUDENT":

        if student.user != request.user:

            messages.error(
                request,
                "You can only view your own information."
            )

            return redirect("dashboard")

    elif request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to view this student."
        )

        return redirect("dashboard")

    return render(
        request,
        "students/student_details.html",
        {
            "student": student
        }
    )