from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Fee
from .forms import FeeForm
from students.models import Student


@login_required
def fee_list(request):

    user = request.user

    if user.role == "ADMIN":

        fees = (
            Fee.objects
            .select_related("student")
            .all()
            .order_by("-id")
        )

        search = request.GET.get("search", "").strip()

        if search:

            fees = fees.filter(
                Q(student__first_name__icontains=search)
                |
                Q(student__last_name__icontains=search)
                |
                Q(receipt_no__icontains=search)
            )

    elif user.role == "STUDENT":

        try:
            student = Student.objects.get(user=user)

        except Student.DoesNotExist:

            messages.error(
                request,
                "Your account is not linked to a student profile."
            )

            return redirect("dashboard")

        fees = (
            Fee.objects
            .select_related("student")
            .filter(student=student)
            .order_by("-id")
        )

        search = ""

    else:

        messages.error(
            request,
            "You do not have permission to access fee information."
        )

        return redirect("dashboard")

    return render(
        request,
        "fees/fee_list.html",
        {
            "fees": fees,
            "search": search
        }
    )


@login_required
def add_fee(request):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can add fee records."
        )

        return redirect("dashboard")

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee added successfully."
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


@login_required
def edit_fee(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can edit fee records."
        )

        return redirect("dashboard")

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
                "Fee updated successfully."
            )

            return redirect("fee_list")

    else:

        form = FeeForm(instance=fee)

    return render(
        request,
        "fees/fee_form.html",
        {
            "form": form,
            "title": "Edit Fee"
        }
    )


@login_required
def delete_fee(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete fee records."
        )

        return redirect("dashboard")

    fee = get_object_or_404(
        Fee.objects.select_related("student"),
        pk=pk
    )

    if request.method == "POST":

        fee.delete()

        messages.success(
            request,
            "Fee deleted successfully."
        )

        return redirect("fee_list")

    return render(
        request,
        "fees/fee_confirm_delete.html",
        {
            "fee": fee
        }
    )


@login_required
def fee_detail(request, pk):

    user = request.user

    if user.role == "ADMIN":

        fee = get_object_or_404(
            Fee.objects.select_related("student"),
            pk=pk
        )

    elif user.role == "STUDENT":

        try:
            student = Student.objects.get(user=user)

        except Student.DoesNotExist:

            messages.error(
                request,
                "Your account is not linked to a student profile."
            )

            return redirect("dashboard")

        fee = get_object_or_404(
            Fee.objects.select_related("student"),
            pk=pk,
            student=student
        )

    else:

        messages.error(
            request,
            "You do not have permission to view fee information."
        )

        return redirect("dashboard")

    return render(
        request,
        "fees/fee_detail.html",
        {
            "fee": fee
        }
    )