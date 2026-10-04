from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Exam
from .forms import ExamForm




@login_required
def exam_list(request):

    # Only valid roles
    if request.user.role not in [
        "ADMIN",
        "TEACHER",
        "STUDENT"
    ]:

        messages.error(
            request,
            "You do not have permission to view exams."
        )

        return redirect("dashboard")


    exams = (
        Exam.objects
        .select_related("subject")
        .all()
        .order_by("-exam_date")
    )



    search = request.GET.get(
        "search",
        ""
    ).strip()


    if search:

        exams = exams.filter(

            Q(
                exam_name__icontains=search
            )

            |

            Q(
                subject__subject_name__icontains=search
            )

        )


    return render(

        request,

        "exams/exam_list.html",

        {
            "exams": exams,
            "search": search
        }

    )




@login_required
def add_exam(request):

    if request.user.role not in [
        "ADMIN",
        "TEACHER"
    ]:

        messages.error(
            request,
            "You do not have permission to add exams."
        )

        return redirect(
            "exam_list"
        )


    if request.method == "POST":

        form = ExamForm(
            request.POST
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Exam added successfully."
            )


            return redirect(
                "exam_list"
            )


    else:

        form = ExamForm()


    return render(

        request,

        "exams/exam_form.html",

        {
            "form": form,
            "title": "Add Exam"
        }

    )




@login_required
def edit_exam(request, pk):

    if request.user.role not in [
        "ADMIN",
        "TEACHER"
    ]:

        messages.error(
            request,
            "You do not have permission to edit exams."
        )

        return redirect(
            "exam_list"
        )


    exam = get_object_or_404(

        Exam.objects.select_related(
            "subject"
        ),

        pk=pk

    )


    if request.method == "POST":

        form = ExamForm(

            request.POST,

            instance=exam

        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Exam updated successfully."
            )


            return redirect(
                "exam_list"
            )


    else:

        form = ExamForm(
            instance=exam
        )


    return render(

        request,

        "exams/exam_form.html",

        {
            "form": form,
            "title": "Edit Exam"
        }

    )



@login_required
def delete_exam(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete exams."
        )

        return redirect(
            "exam_list"
        )


    exam = get_object_or_404(

        Exam.objects.select_related(
            "subject"
        ),

        pk=pk

    )



    if request.method == "POST":

        exam.delete()


        messages.success(
            request,
            "Exam deleted successfully."
        )


        return redirect(
            "exam_list"
        )


    return render(

        request,

        "exams/exam_confirm_delete.html",

        {
            "exam": exam
        }

    )




@login_required
def exam_detail(request, pk):

    if request.user.role not in [
        "ADMIN",
        "TEACHER",
        "STUDENT"
    ]:

        messages.error(
            request,
            "You do not have permission to view this exam."
        )

        return redirect(
            "dashboard"
        )


    exam = get_object_or_404(

        Exam.objects.select_related(
            "subject"
        ),

        pk=pk

    )


    return render(

        request,

        "exams/exam_detail.html",

        {
            "exam": exam
        }

    )