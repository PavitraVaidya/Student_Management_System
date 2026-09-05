from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
    "admission_no",
    "first_name",
    "last_name",
    "dob",
    "gender",
    "phone",
    "email",
    "address",
    "parent_name",
    "course",
    "photo",
]

        widgets = {

            "admission_no": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "first_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "last_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "dob": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "gender": forms.Select(attrs={
                "class": "form-select"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "parent_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "course": forms.Select(attrs={
                "class": "form-select"
            }),

            "photo": forms.FileInput(attrs={
                "class": "form-control"
            })

        }