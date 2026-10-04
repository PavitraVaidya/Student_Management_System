from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Result
from .forms import ResultForm
from students.models import Student


# =========================================================
# RESULT LIST
#
# ADMIN   -> All results
# TEACHER -> All results
# STUDENT -> Own results only
# =========================================================

@login_required
def result_list(request):

    user = request.user


    # -----------------------------------------------------
    # ADMIN / TEACHER
    # -----------------------------------------------------

    if user.role in ["ADMIN", "TEACHER"]:

        results = (
            Result.objects
            .select_related(
                "student",
                "exam",
                "exam__subject"
            )
            .all()
            .order_by("-id")
        )


        search = request.GET.get(
            "search",
            ""
        ).strip()


        if search:

            results = results.filter(

                Q(
                    student__first_name__icontains=search
                )

                |

                Q(
                    student__last_name__icontains=search
                )

                |

                Q(
                    exam__exam_name__icontains=search
                )

                |

                Q(
                    exam__subject__subject_name__icontains=search
                )

            )


    # -----------------------------------------------------
    # STUDENT
    # -----------------------------------------------------

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

            return redirect(
                "dashboard"
            )


        # Only logged-in student's results

        results = (
            Result.objects
            .select_related(
                "student",
                "exam",
                "exam__subject"
            )
            .filter(
                student=student
            )
            .order_by("-id")
        )


        search = ""


    # -----------------------------------------------------
    # INVALID ROLE
    # -----------------------------------------------------

    else:

        messages.error(
            request,
            "You do not have permission to view results."
        )

        return redirect(
            "dashboard"
        )


    return render(

        request,

        "results/result_list.html",

        {
            "results": results,
            "search": search
        }

    )


# =========================================================
# ADD RESULT
#
# ADMIN   -> Yes
# TEACHER -> Yes
# STUDENT -> No
# =========================================================

@login_required
def add_result(request):

    if request.user.role not in [
        "ADMIN",
        "TEACHER"
    ]:

        messages.error(
            request,
            "You do not have permission to add results."
        )

        return redirect(
            "result_list"
        )


    if request.method == "POST":

        form = ResultForm(
            request.POST
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Result added successfully."
            )


            return redirect(
                "result_list"
            )


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


# =========================================================
# EDIT RESULT
#
# ADMIN   -> Yes
# TEACHER -> Yes
# STUDENT -> No
# =========================================================

@login_required
def edit_result(request, pk):

    if request.user.role not in [
        "ADMIN",
        "TEACHER"
    ]:

        messages.error(
            request,
            "You do not have permission to edit results."
        )

        return redirect(
            "result_list"
        )


    result = get_object_or_404(

        Result.objects.select_related(
            "student",
            "exam",
            "exam__subject"
        ),

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
                "Result updated successfully."
            )


            return redirect(
                "result_list"
            )


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


# =========================================================
# DELETE RESULT
#
# ADMIN ONLY
# =========================================================

@login_required
def delete_result(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete results."
        )

        return redirect(
            "result_list"
        )


    result = get_object_or_404(

        Result.objects.select_related(
            "student",
            "exam"
        ),

        pk=pk

    )


    # Delete only after POST confirmation

    if request.method == "POST":

        result.delete()


        messages.success(
            request,
            "Result deleted successfully."
        )


        return redirect(
            "result_list"
        )


    return render(

        request,

        "results/result_confirm_delete.html",

        {
            "result": result
        }

    )


# =========================================================
# RESULT DETAIL
#
# ADMIN   -> Any result
# TEACHER -> Any result
# STUDENT -> Own result only
# =========================================================

@login_required
def result_detail(request, pk):

    user = request.user


    # -----------------------------------------------------
    # ADMIN / TEACHER
    # -----------------------------------------------------

    if user.role in [
        "ADMIN",
        "TEACHER"
    ]:

        result = get_object_or_404(

            Result.objects.select_related(
                "student",
                "exam",
                "exam__subject"
            ),

            pk=pk

        )


    # -----------------------------------------------------
    # STUDENT
    # -----------------------------------------------------

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

            return redirect(
                "dashboard"
            )


        # SECURITY:
        # Result must belong to logged-in student

        result = get_object_or_404(

            Result.objects.select_related(
                "student",
                "exam",
                "exam__subject"
            ),

            pk=pk,

            student=student

        )


    # -----------------------------------------------------
    # INVALID ROLE
    # -----------------------------------------------------

    else:

        messages.error(
            request,
            "You do not have permission to view this result."
        )

        return redirect(
            "dashboard"
        )


    return render(

        request,

        "results/result_detail.html",

        {
            "result": result
        }

    )