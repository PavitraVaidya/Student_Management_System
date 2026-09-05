from django import forms
from .models import Teacher


class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        fields = [
            "teacher_id",
            "first_name",
            "last_name",
            "qualification",
            "experience",
            "phone",
            "email",
            "subject",
        ]

        widgets = {

            "teacher_id": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "qualification": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "experience": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "subject": forms.Select(attrs={
                "class": "form-select"
            }),

        }