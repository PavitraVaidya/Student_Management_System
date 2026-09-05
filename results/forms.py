from django import forms
from .models import Result


class ResultForm(forms.ModelForm):

    class Meta:

        model = Result

        fields = [
            "student",
            "exam",
            "marks",
        ]

        widgets = {

            "student": forms.Select(attrs={
                "class": "form-select"
            }),

            "exam": forms.Select(attrs={
                "class": "form-select"
            }),

            "marks": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0
            }),

        }