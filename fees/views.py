from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Fee
from .forms import FeeForm


def fee_list(request):

    fees = Fee.objects.select_related(
        "student"
    ).all().order_by("-id")

    search = request.GET.get("search")

    if search:
        fees = fees.filter(
            Q(student__first_name__icontains=search) |
            Q(student__last_name__icontains=search) |
            Q(receipt_no__icontains=search)
        )

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees
        }
    )


def add_fee(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee Added Successfully."
            )

            return redirect("fee_list")

    else:
        form = FeeForm()

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form,
            "title": "Add Fee"
        }
    )


def edit_fee(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    if request.method == "POST":

        form = FeeForm(
            request.POST,
            instance=fee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee Updated Successfully."
            )

            return redirect("fee_list")

    else:

        form = FeeForm(
            instance=fee
        )

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form,
            "title": "Edit Fee"
        }
    )


def delete_fee(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    fee.delete()

    messages.success(
        request,
        "Fee Deleted Successfully."
    )

    return redirect("fee_list")


def fee_detail(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    return render(
        request,
        "fees/fee_detail.html",
        {
            "fee": fee
        }
    )