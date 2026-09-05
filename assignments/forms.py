from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = [
            "student",
            "subject",
            "teacher",
            "title",
            "description",
            "due_date",
            "submission_date",
            "status",
            "marks",
        ]

        widgets = {

            "student": forms.Select(attrs={
                "class": "form-select"
            }),

            "subject": forms.Select(attrs={
                "class": "form-select"
            }),

            "teacher": forms.Select(attrs={
                "class": "form-select"
            }),

            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "submission_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "marks": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

        }