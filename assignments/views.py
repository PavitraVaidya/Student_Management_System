
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Assignment
from .forms import AssignmentForm


def assignment_list(request):

    assignments = Assignment.objects.select_related(
        "student",
        "subject",
        "teacher"
    ).all().order_by("-id")

    search = request.GET.get("search")

    if search:
        assignments = assignments.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(subject__subject_name__icontains=search) |
            Q(title__icontains=search)
        )

    return render(
        request,
        "assignments/assignment_list.html",
        {
            "assignments": assignments
        }
    )


def add_assignment(request):

    if request.method == "POST":

        form = AssignmentForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Assignment Added Successfully."
            )

            return redirect("assignment_list")

    else:

        form = AssignmentForm()

    return render(
        request,
        "assignments/assignment_form.html",
        {
            "form": form,
            "title": "Add Assignment"
        }
    )


def edit_assignment(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    if request.method == "POST":

        form = AssignmentForm(
            request.POST,
            instance=assignment
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Assignment Updated Successfully."
            )

            return redirect("assignment_list")

    else:

        form = AssignmentForm(
            instance=assignment
        )

    return render(
        request,
        "assignments/assignment_form.html",
        {
            "form": form,
            "title": "Edit Assignment"
        }
    )


def delete_assignment(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    assignment.delete()

    messages.success(
        request,
        "Assignment Deleted Successfully."
    )

    return redirect("assignment_list")


def assignment_detail(request, pk):

    assignment = get_object_or_404(
        Assignment,
        pk=pk
    )

    return render(
        request,
        "assignments/assignment_detail.html",
        {
            "assignment": assignment
        }
    )