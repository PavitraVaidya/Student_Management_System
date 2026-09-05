from django import forms
from .models import Course


class CourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = [
            "course_name",
            "course_code",
            "duration",
            "total_semesters",
        ]

        widgets = {

            "course_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "course_code": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "duration": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "total_semesters": forms.NumberInput(attrs={
                "class": "form-control"
            }),

        }