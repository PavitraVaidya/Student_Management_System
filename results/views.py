from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Result
from .forms import ResultForm


def result_list(request):

    results = Result.objects.select_related(
        "student",
        "exam",
        "exam__subject"
    ).all().order_by("-id")

    search = request.GET.get("search")

    if search:
        results = results.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(exam__exam_name__icontains=search)
        )

    return render(
        request,
        "results/result_list.html",
        {
            "results": results
        }
    )


def add_result(request):

    if request.method == "POST":

        form = ResultForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Result Added Successfully."
            )

            return redirect("result_list")

    else:
        form = ResultForm()

    return render(
        request,
        "results/result_form.html",
        {
            "form": form,
            "title": "Add Result"
        }
    )


def edit_result(request, pk):

    result = get_object_or_404(
        Result,
        pk=pk
    )

    if request.method == "POST":

        form = ResultForm(
            request.POST,
            instance=result
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Result Updated Successfully."
            )

            return redirect("result_list")

    else:

        form = ResultForm(
            instance=result
        )

    return render(
        request,
        "results/result_form.html",
        {
            "form": form,
            "title": "Edit Result"
        }
    )


def delete_result(request, pk):

    result = get_object_or_404(
        Result,
        pk=pk
    )

    result.delete()

    messages.success(
        request,
        "Result Deleted Successfully."
    )

    return redirect("result_list")


def result_detail(request, pk):

    result = get_object_or_404(
        Result,
        pk=pk
    )

    return render(
        request,
        "results/result_detail.html",
        {
            "result": result
        }
    )
