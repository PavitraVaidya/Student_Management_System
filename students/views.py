from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from accounts.models import User
from .models import Student
from .forms import StudentForm


# -----------------------------
# Student List
# -----------------------------
def student_list(request):

    students = Student.objects.select_related("course").all().order_by("-id")

    search = request.GET.get("search")

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

    return render(request, "students/student_list.html", context)


# -----------------------------
# Add Student
# -----------------------------
def add_student(request):

    if request.method == "POST":

        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():

            student = form.save(commit=False)

            username = student.admission_no.lower()

            password = "Student@123"

            user = User.objects.create(
                username=username,
                email=student.email,
                password=make_password(password),
                role="STUDENT"
            )

            student.user = user
            student.save()

            messages.success(request, "Student Added Successfully.")

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


# -----------------------------
# Edit Student
# -----------------------------
def edit_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(request, "Student Updated Successfully.")

            return redirect("student_list")

    else:

        form = StudentForm(instance=student)

    return render(
        request,
        "students/student_form.html",
        {
            "form": form,
            "title": "Edit Student"
        }
    )


# -----------------------------
# Delete Student
# -----------------------------
def delete_student(request, pk):

    student = get_object_or_404(Student, pk=pk)

    student.delete()

    messages.success(request, "Student Deleted Successfully.")

    return redirect("student_list")


# -----------------------------
# Student Details
# -----------------------------
def student_detail(request, pk):

    student = get_object_or_404(Student, pk=pk)

    return render(
        request,
        "students/student_details.html",
        {
            "student": student
        }
    )