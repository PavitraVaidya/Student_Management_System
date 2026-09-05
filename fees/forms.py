from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):

    class Meta:

        model = Fee

        fields = [
            "student",
            "receipt_no",
            "amount",
            "due_date",
            "payment_date",
            "status",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(attrs={
                "class": "form-select"
            }),

            "receipt_no": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "due_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "payment_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "status": forms.Select(attrs={
                "class": "form-select"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }