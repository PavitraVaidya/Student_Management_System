from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Assignment
from .forms import AssignmentForm
from students.models import Student


@login_required
def assignment_list(request):

    user = request.user

    if user.role in ["ADMIN", "TEACHER"]:

        assignments = (
            Assignment.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .all()
            .order_by("-id")
        )

        search = request.GET.get("search", "").strip()

        if search:

            assignments = assignments.filter(
                Q(student__first_name__icontains=search)
                |
                Q(student__last_name__icontains=search)
                |
                Q(subject__subject_name__icontains=search)
                |
                Q(title__icontains=search)
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

        assignments = (
            Assignment.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .filter(
                student=student
            )
            .order_by("-id")
        )

        search = ""

    else:

        messages.error(
            request,
            "You do not have permission to view assignments."
        )

        return redirect("dashboard")

    return render(
        request,
        "assignments/assignment_list.html",
        {
            "assignments": assignments,
            "search": search
        }
    )


@login_required
def add_assignment(request):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to add assignments."
        )

        return redirect("dashboard")

    if request.method == "POST":

        form = AssignmentForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Assignment added successfully."
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


@login_required
def edit_assignment(request, pk):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to edit assignments."
        )

        return redirect("dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related(
            "student",
            "subject",
            "teacher"
        ),
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
                "Assignment updated successfully."
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


@login_required
def delete_assignment(request, pk):

    if request.user.role not in ["ADMIN", "TEACHER"]:

        messages.error(
            request,
            "You do not have permission to delete assignments."
        )

        return redirect("dashboard")

    assignment = get_object_or_404(
        Assignment.objects.select_related(
            "student",
            "subject",
            "teacher"
        ),
        pk=pk
    )

    if request.method == "POST":

        assignment.delete()

        messages.success(
            request,
            "Assignment deleted successfully."
        )

        return redirect("assignment_list")

    return render(
        request,
        "assignments/assignment_confirm_delete.html",
        {
            "assignment": assignment
        }
    )


@login_required
def assignment_detail(request, pk):

    user = request.user

    if user.role in ["ADMIN", "TEACHER"]:

        assignment = get_object_or_404(
            Assignment.objects.select_related(
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

        assignment = get_object_or_404(
            Assignment.objects.select_related(
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
            "You do not have permission to view this assignment."
        )

        return redirect("dashboard")

    return render(
        request,
        "assignments/assignment_detail.html",
        {
            "assignment": assignment
        }
    )