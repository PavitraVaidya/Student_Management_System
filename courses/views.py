from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Course
from .forms import CourseForm


@login_required
def course_list(request):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to view courses."
        )

        return redirect("dashboard")

    courses = (
        Course.objects
        .all()
        .order_by("-id")
    )

    search = request.GET.get("search", "").strip()

    if search:

        courses = courses.filter(
            Q(course_name__icontains=search)
            |
            Q(course_code__icontains=search)
        )

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
            "search": search
        }
    )


@login_required
def add_course(request):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can add courses."
        )

        return redirect("course_list")

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course added successfully."
            )

            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Add Course"
        }
    )


@login_required
def edit_course(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can edit courses."
        )

        return redirect("course_list")

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course updated successfully."
            )

            return redirect("course_list")

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Edit Course"
        }
    )


@login_required
def delete_course(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete courses."
        )

        return redirect("course_list")

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect("course_list")

    return render(
        request,
        "courses/course_confirm_delete.html",
        {
            "course": course
        }
    )


@login_required
def course_detail(request, pk):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to view course details."
        )

        return redirect("dashboard")

    course = get_object_or_404(
        Course,
        pk=pk
    )

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course
        }
    )