from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import User
from .models import Teacher
from .forms import TeacherForm



@login_required
def teacher_list(request):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can view the teacher list."
        )

        return redirect("dashboard")


    teachers = (
        Teacher.objects
        .select_related(
            "subject",
            "user"
        )
        .all()
        .order_by("-id")
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = request.GET.get(
        "search",
        ""
    ).strip()


    if search:

        teachers = teachers.filter(

            Q(first_name__icontains=search)

            |

            Q(last_name__icontains=search)

            |

            Q(teacher_id__icontains=search)

            |

            Q(phone__icontains=search)

        )


    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": teachers,
            "search": search
        }
    )




@login_required
def add_teacher(request):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can add teachers."
        )

        return redirect("dashboard")


    if request.method == "POST":

        form = TeacherForm(request.POST)


        if form.is_valid():

            teacher = form.save(
                commit=False
            )



            username = (
                teacher.teacher_id
                .lower()
            )



            password = "Teacher@123"


          

            if User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    "A user with this Teacher ID already exists."
                )

                return render(
                    request,
                    "teachers/teacher_form.html",
                    {
                        "form": form,
                        "title": "Add Teacher"
                    }
                )



            user = User.objects.create(

                username=username,

                email=teacher.email,

                password=make_password(
                    password
                ),

                role="TEACHER"

            )


            # Connect teacher to login account

            teacher.user = user

            teacher.save()


            messages.success(
                request,
                f"Teacher added successfully. "
                f"Username: {username} | "
                f"Default Password: {password}"
            )


            return redirect(
                "teacher_list"
            )


    else:

        form = TeacherForm()


    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Add Teacher"
        }
    )




@login_required
def edit_teacher(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can edit teachers."
        )

        return redirect("dashboard")


    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )


    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            instance=teacher
        )


        if form.is_valid():

            updated_teacher = form.save()


   
            if updated_teacher.user:

                updated_teacher.user.email = (
                    updated_teacher.email
                )

                updated_teacher.user.save()


            messages.success(
                request,
                "Teacher updated successfully."
            )


            return redirect(
                "teacher_list"
            )


    else:

        form = TeacherForm(
            instance=teacher
        )


    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Edit Teacher"
        }
    )




@login_required
def delete_teacher(request, pk):

    if request.user.role != "ADMIN":

        messages.error(
            request,
            "Only administrators can delete teachers."
        )

        return redirect("dashboard")


    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )



    if request.method == "POST":


        user = teacher.user


        teacher.delete()



        if user:

            user.delete()


        messages.success(
            request,
            "Teacher deleted successfully."
        )


        return redirect(
            "teacher_list"
        )


    return render(
        request,
        "teachers/teacher_confirm_delete.html",
        {
            "teacher": teacher
        }
    )




@login_required
def teacher_detail(request, pk):

    user = request.user


  

    if user.role == "ADMIN":

        teacher = get_object_or_404(

            Teacher.objects.select_related(
                "subject",
                "user"
            ),

            pk=pk

        )


   

    elif user.role == "TEACHER":

      

        teacher = get_object_or_404(

            Teacher.objects.select_related(
                "subject",
                "user"
            ),

            pk=pk,

            user=user

        )


   
    else:

        messages.error(
            request,
            "You do not have permission to view teacher information."
        )

        return redirect(
            "dashboard"
        )


    return render(
        request,
        "teachers/teacher_detail.html",
        {
            "teacher": teacher
        }
    )