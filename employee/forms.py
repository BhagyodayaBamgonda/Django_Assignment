from django import forms
from .models import Employee, Leave


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = "__all__"


class LeaveForm(forms.ModelForm):

    class Meta:
        model = Leave
        fields = "__all__"

    def clean(self):

        cleaned_data = super().clean()

        from_date = cleaned_data.get("from_date")
        to_date = cleaned_data.get("to_date")

        if from_date and to_date:
            if from_date > to_date:
                raise forms.ValidationError(
                    "From Date cannot be greater than To Date."
                )

        return cleaned_data