from django import forms
from .models import Exam


class ExamForm(forms.ModelForm):

    class Meta:

        model = Exam

        fields = [
            "exam_name",
            "subject",
            "exam_date",
            "total_marks",
            "passing_marks",
            "description",
        ]

        widgets = {

            "exam_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "subject": forms.Select(attrs={
                "class": "form-select"
            }),

            "exam_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "total_marks": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "passing_marks": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }