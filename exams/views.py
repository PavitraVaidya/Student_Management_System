from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Exam
from .forms import ExamForm


def exam_list(request):

    exams = Exam.objects.select_related(
        "subject"
    ).all().order_by("-exam_date")

    search = request.GET.get("search")

    if search:
        exams = exams.filter(
            Q(exam_name__icontains=search) |
            Q(subject__subject_name__icontains=search)
        )

    return render(
        request,
        "exams/exam_list.html",
        {
            "exams": exams
        }
    )


def add_exam(request):

    if request.method == "POST":

        form = ExamForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Exam Added Successfully."
            )

            return redirect("exam_list")

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


def edit_exam(request, pk):

    exam = get_object_or_404(
        Exam,
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
                "Exam Updated Successfully."
            )

            return redirect("exam_list")

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


def delete_exam(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )

    exam.delete()

    messages.success(
        request,
        "Exam Deleted Successfully."
    )

    return redirect("exam_list")


def exam_detail(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )

    return render(
        request,
        "exams/exam_detail.html",
        {
            "exam": exam
        }
    )
