from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Course
from .forms import CourseForm


def course_list(request):

    courses = Course.objects.all().order_by("-id")

    search = request.GET.get("search")

    if search:
        courses = courses.filter(
            Q(course_name__icontains=search) |
            Q(course_code__icontains=search)
        )

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )


def add_course(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Course Added Successfully."
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


def edit_course(request, pk):

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
                "Course Updated Successfully."
            )

            return redirect("course_list")

    else:

        form = CourseForm(instance=course)

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Edit Course"
        }
    )


def delete_course(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    course.delete()

    messages.success(
        request,
        "Course Deleted Successfully."
    )

    return redirect("course_list")


def course_detail(request, pk):

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
