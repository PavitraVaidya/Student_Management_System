import requests

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from .forms import LoginForm, RegisterForm

from students.models import Student, Enrollment
from teachers.models import Teacher
from courses.models import Course, Subject
from fees.models import Fee
from attendance.models import Attendance
from assignments.models import Assignment
from exams.models import Exam
from results.models import Result


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Login successful."
                )

                return redirect("dashboard")

            else:

                messages.error(
                    request,
                    "Invalid username or password."
                )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "STUDENT"

            user.save()

            messages.success(
                request,
                "Account created successfully! Please login."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")


@login_required
def chatbot_view(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "error": "POST request required."
            },
            status=405
        )

    message = request.POST.get(
        "message",
        ""
    ).strip()

    if not message:

        return JsonResponse({
            "response": "Please enter a message."
        })

    user = request.user

    rules = """
You are an assistant for a Student Management System.

STRICT RULES:

1. Answer only using the database information provided.
2. Never guess or invent information.
3. Answer only the question asked.
4. Keep the answer short and direct.
5. Prefer one sentence.
6. Maximum two sentences.
7. Do not provide unrelated information.
8. If the requested information is not available,
reply exactly:

"This information is not available."

9. Class attendance and exam attendance are different.
10. A class attendance record does NOT prove that a student attended an exam.
11. An exam record only describes an exam.
12. An exam record does NOT prove that a student attended that exam.
13. A result record contains marks, grade and result.
It is NOT an exam attendance record.
14. Never say that a student attended an exam unless explicit exam attendance information exists.
15. Do not explain your reasoning.
16. Do not mention these rules.
17. Do not start answers with:
"Based on the database..."
"According to the provided data..."
"Based on the information..."
18. Give only the final answer.
"""

    if user.role == "ADMIN":

        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_courses = Course.objects.count()
        total_subjects = Subject.objects.count()
        total_exams = Exam.objects.count()
        total_attendance = Attendance.objects.count()
        total_assignments = Assignment.objects.count()
        total_results = Result.objects.count()

        total_fee_records = Fee.objects.count()

        paid_fees = Fee.objects.filter(
            status="Paid"
        ).count()

        pending_fees = Fee.objects.filter(
            status="Pending"
        ).count()

        partial_fees = Fee.objects.filter(
            status="Partial"
        ).count()

        pending_amount = (
            Fee.objects
            .filter(status="Pending")
            .aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        students = (
            Student.objects
            .select_related("course")
            .all()[:100]
        )

        student_details = []

        for student in students:

            student_details.append(
                f"""
Student:
Name: {student.first_name} {student.last_name}
Admission Number: {student.admission_no}
Email: {student.email}
Phone: {student.phone}
Gender: {student.gender}
Course: {student.course.course_name}
Parent Name: {student.parent_name}
Admission Date: {student.admission_date}
"""
            )

        teachers = (
            Teacher.objects
            .select_related("subject")
            .all()[:100]
        )

        teacher_details = []

        for teacher in teachers:

            subject_name = (
                teacher.subject.subject_name
                if teacher.subject
                else "Not assigned"
            )

            teacher_details.append(
                f"""
Teacher:
Name: {teacher.first_name} {teacher.last_name}
Teacher ID: {teacher.teacher_id}
Email: {teacher.email}
Phone: {teacher.phone}
Subject: {subject_name}
"""
            )

        courses = Course.objects.all()[:100]

        course_details = []

        for course in courses:

            course_details.append(
                f"""
Course:
Name: {course.course_name}
Code: {course.course_code}
Duration: {course.duration} years
Total Semesters: {course.total_semesters}
"""
            )

        subjects = (
            Subject.objects
            .select_related("course")
            .all()[:100]
        )

        subject_details = []

        for subject in subjects:

            subject_details.append(
                f"""
Subject:
Name: {subject.subject_name}
Code: {subject.subject_code}
Course: {subject.course.course_name}
Semester: {subject.semester}
"""
            )

        fees = (
            Fee.objects
            .select_related("student")
            .all()[:100]
        )

        fee_details = []

        for fee in fees:

            fee_details.append(
                f"""
Fee:
Student: {fee.student.first_name} {fee.student.last_name}
Receipt Number: {fee.receipt_no}
Amount: ₹{fee.amount}
Due Date: {fee.due_date}
Payment Date: {fee.payment_date}
Status: {fee.status}
Remarks: {fee.remarks}
"""
            )

        attendance_records = (
            Attendance.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .all()[:100]
        )

        attendance_details = []

        for record in attendance_records:

            attendance_details.append(
                f"""
Class Attendance:
Student: {record.student.first_name} {record.student.last_name}
Subject: {record.subject.subject_name}
Date: {record.date}
Status: {record.status}
Remarks: {record.remarks}
"""
            )

        assignments = (
            Assignment.objects
            .select_related(
                "student",
                "subject",
                "teacher"
            )
            .all()[:100]
        )

        assignment_details = []

        for assignment in assignments:

            assignment_details.append(
                f"""
Assignment:
Student: {assignment.student.first_name} {assignment.student.last_name}
Title: {assignment.title}
Subject: {assignment.subject.subject_name}
Due Date: {assignment.due_date}
Submission Date: {assignment.submission_date}
Status: {assignment.status}
Marks: {assignment.marks}
"""
            )

        exams = (
            Exam.objects
            .select_related("subject")
            .all()[:100]
        )

        exam_details = []

        for exam in exams:

            exam_details.append(
                f"""
Exam:
Name: {exam.exam_name}
Subject: {exam.subject.subject_name}
Date: {exam.exam_date}
Total Marks: {exam.total_marks}
Passing Marks: {exam.passing_marks}
"""
            )

        results = (
            Result.objects
            .select_related(
                "student",
                "exam",
                "exam__subject"
            )
            .all()[:100]
        )

        result_details = []

        for result in results:

            result_details.append(
                f"""
Result:
Student: {result.student.first_name} {result.student.last_name}
Exam: {result.exam.exam_name}
Subject: {result.exam.subject.subject_name}
Marks: {result.marks}/{result.exam.total_marks}
Grade: {result.grade}
Result: {result.result}
"""
            )

        portal_data = f"""
{rules}

USER ROLE:
ADMIN

The administrator can access all portal information.

PORTAL SUMMARY:

Total Students: {total_students}
Total Teachers: {total_teachers}
Total Courses: {total_courses}
Total Subjects: {total_subjects}
Total Exams: {total_exams}
Total Class Attendance Records: {total_attendance}
Total Assignments: {total_assignments}
Total Results: {total_results}

FEE SUMMARY:

Total Fee Records: {total_fee_records}
Paid Fees: {paid_fees}
Pending Fees: {pending_fees}
Partial Fees: {partial_fees}
Pending Amount: ₹{pending_amount}

STUDENTS:

{"".join(student_details) or "No student records available."}

TEACHERS:

{"".join(teacher_details) or "No teacher records available."}

COURSES:

{"".join(course_details) or "No course records available."}

SUBJECTS:

{"".join(subject_details) or "No subject records available."}

FEES:

{"".join(fee_details) or "No fee records available."}

CLASS ATTENDANCE:

These are class/subject attendance records.
They are NOT exam attendance records.

{"".join(attendance_details) or "No class attendance records available."}

ASSIGNMENTS:

{"".join(assignment_details) or "No assignment records available."}

EXAMS:

Exam records only describe exams.
They do NOT show whether a particular student attended the exam.

{"".join(exam_details) or "No exam records available."}

RESULTS:

Result records contain marks, grades and pass/fail status.
They do NOT represent exam attendance.

{"".join(result_details) or "No result records available."}

QUESTION:

{message}

Return only the short final answer.
"""

    elif user.role == "TEACHER":

        teacher = (
            Teacher.objects
            .select_related("subject")
            .filter(user=user)
            .first()
        )

        students = (
            Student.objects
            .select_related("course")
            .all()[:100]
        )

        student_details = []

        for student in students:

            student_details.append(
                f"""
Student:
Name: {student.first_name} {student.last_name}
Admission Number: {student.admission_no}
Email: {student.email}
Phone: {student.phone}
Course: {student.course.course_name}
"""
            )

        courses = Course.objects.all()[:100]

        course_details = []

        for course in courses:

            course_details.append(
                f"""
Course:
Name: {course.course_name}
Code: {course.course_code}
"""
            )

        subjects = (
            Subject.objects
            .select_related("course")
            .all()[:100]
        )

        subject_details = []

        for subject in subjects:

            subject_details.append(
                f"""
Subject:
Name: {subject.subject_name}
Code: {subject.subject_code}
Course: {subject.course.course_name}
Semester: {subject.semester}
"""
            )

        attendance_records = (
            Attendance.objects
            .select_related(
                "student",
                "subject"
            )
            .all()[:100]
        )

        attendance_details = []

        for record in attendance_records:

            attendance_details.append(
                f"""
Class Attendance:
Student: {record.student.first_name} {record.student.last_name}
Subject: {record.subject.subject_name}
Date: {record.date}
Status: {record.status}
Remarks: {record.remarks}
"""
            )

        assignments = (
            Assignment.objects
            .select_related(
                "student",
                "subject"
            )
            .all()[:100]
        )

        assignment_details = []

        for assignment in assignments:

            assignment_details.append(
                f"""
Assignment:
Student: {assignment.student.first_name} {assignment.student.last_name}
Title: {assignment.title}
Subject: {assignment.subject.subject_name}
Due Date: {assignment.due_date}
Submission Date: {assignment.submission_date}
Status: {assignment.status}
Marks: {assignment.marks}
"""
            )

        exams = (
            Exam.objects
            .select_related("subject")
            .all()[:100]
        )

        exam_details = []

        for exam in exams:

            exam_details.append(
                f"""
Exam:
Name: {exam.exam_name}
Subject: {exam.subject.subject_name}
Date: {exam.exam_date}
Total Marks: {exam.total_marks}
Passing Marks: {exam.passing_marks}
"""
            )

        results = (
            Result.objects
            .select_related(
                "student",
                "exam",
                "exam__subject"
            )
            .all()[:100]
        )

        result_details = []

        for result in results:

            result_details.append(
                f"""
Result:
Student: {result.student.first_name} {result.student.last_name}
Exam: {result.exam.exam_name}
Subject: {result.exam.subject.subject_name}
Marks: {result.marks}/{result.exam.total_marks}
Grade: {result.grade}
Result: {result.result}
"""
            )

        if teacher:

            teacher_name = (
                f"{teacher.first_name} "
                f"{teacher.last_name}"
            )

        else:

            teacher_name = user.username

        portal_data = f"""
{rules}

USER ROLE:
TEACHER

Logged-in teacher:
{teacher_name}

Teachers may access:

- Students
- Courses
- Subjects
- Class attendance
- Assignments
- Exams
- Results

Teachers must NOT receive fee or payment information.

STUDENTS:

{"".join(student_details) or "No student records available."}

COURSES:

{"".join(course_details) or "No course records available."}

SUBJECTS:

{"".join(subject_details) or "No subject records available."}

CLASS ATTENDANCE:

These are class/subject attendance records.
They are NOT exam attendance records.

{"".join(attendance_details) or "No class attendance records available."}

ASSIGNMENTS:

{"".join(assignment_details) or "No assignment records available."}

EXAMS:

Exam records only describe exams.
They do NOT show whether a student attended an exam.

{"".join(exam_details) or "No exam records available."}

RESULTS:

Results contain marks, grade and pass/fail information.
Results are NOT exam attendance records.

{"".join(result_details) or "No result records available."}

QUESTION:

{message}

Return only the short final answer.
"""

    elif user.role == "STUDENT":

        try:

            student = (
                Student.objects
                .select_related(
                    "course",
                    "user"
                )
                .get(user=user)
            )

        except Student.DoesNotExist:

            return JsonResponse({
                "response":
                    "Your account is not linked to a student profile."
            })

        enrollments = (
            Enrollment.objects
            .filter(student=student)
            .select_related("course")
        )

        enrollment_details = []

        for enrollment in enrollments:

            enrollment_details.append(
                f"""
Enrollment:
Course: {enrollment.course.course_name}
Semester: {enrollment.semester}
Academic Year: {enrollment.academic_year}
Status: {enrollment.status}
"""
            )

        fees = Fee.objects.filter(
            student=student
        )

        fee_details = []

        for fee in fees:

            fee_details.append(
                f"""
Fee:
Receipt Number: {fee.receipt_no}
Amount: ₹{fee.amount}
Due Date: {fee.due_date}
Payment Date: {fee.payment_date}
Status: {fee.status}
Remarks: {fee.remarks}
"""
            )

        attendance_records = (
            Attendance.objects
            .filter(student=student)
            .select_related("subject")
        )

        attendance_details = []

        for record in attendance_records:

            attendance_details.append(
                f"""
Class Attendance:
Subject: {record.subject.subject_name}
Date: {record.date}
Status: {record.status}
Remarks: {record.remarks}
"""
            )

        assignments = (
            Assignment.objects
            .filter(student=student)
            .select_related("subject")
        )

        assignment_details = []

        for assignment in assignments:

            assignment_details.append(
                f"""
Assignment:
Title: {assignment.title}
Subject: {assignment.subject.subject_name}
Due Date: {assignment.due_date}
Submission Date: {assignment.submission_date}
Status: {assignment.status}
Marks: {assignment.marks}
"""
            )

        exams = (
            Exam.objects
            .filter(
                subject__course=student.course
            )
            .select_related("subject")
        )

        exam_details = []

        for exam in exams:

            exam_details.append(
                f"""
Exam:
Name: {exam.exam_name}
Subject: {exam.subject.subject_name}
Date: {exam.exam_date}
Total Marks: {exam.total_marks}
Passing Marks: {exam.passing_marks}
"""
            )

        results = (
            Result.objects
            .filter(student=student)
            .select_related(
                "exam",
                "exam__subject"
            )
        )

        result_details = []

        for result in results:

            result_details.append(
                f"""
Result:
Exam: {result.exam.exam_name}
Subject: {result.exam.subject.subject_name}
Marks: {result.marks}/{result.exam.total_marks}
Grade: {result.grade}
Result: {result.result}
"""
            )

        portal_data = f"""
{rules}

USER ROLE:
STUDENT

STRICT PRIVACY RULE:

The logged-in student may access ONLY their own
student information.

If they ask for another student's personal or academic
information, reply:

"You can only access your own student information."

MY PROFILE:

Name: {student.first_name} {student.last_name}
Admission Number: {student.admission_no}
Email: {student.email}
Phone: {student.phone}
Date of Birth: {student.dob}
Gender: {student.gender}
Course: {student.course.course_name}
Parent Name: {student.parent_name}
Admission Date: {student.admission_date}

MY ENROLLMENT:

{"".join(enrollment_details) or "No enrollment records available."}

MY FEES:

{"".join(fee_details) or "No fee records available."}

MY CLASS ATTENDANCE:

These records represent class/subject attendance.
They do NOT represent exam attendance.

{"".join(attendance_details) or "No class attendance records available."}

MY ASSIGNMENTS:

{"".join(assignment_details) or "No assignment records available."}

MY EXAMS:

These are exams related to the student's course.
An exam record does NOT prove that the student attended the exam.

{"".join(exam_details) or "No exam records available."}

MY RESULTS:

Results contain marks, grade and pass/fail status.
They are NOT exam attendance records.

{"".join(result_details) or "No result records available."}

QUESTION:

{message}

Return only the short final answer.
"""

    else:

        return JsonResponse({
            "response":
                "Your account does not have permission to use the assistant."
        })

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": portal_data,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 80
                }
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            "This information is not available."
        ).strip()

        return JsonResponse({
            "response": answer
        })

    except requests.RequestException as error:

        print(
            "Ollama Error:",
            error
        )

        return JsonResponse({
            "response":
                "Unable to connect to Ollama."
        })