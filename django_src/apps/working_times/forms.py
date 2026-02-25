from django import forms
from .models import WorkingTime


class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = ["from_time", "to_time"]

    def clean(self):
        cleaned_data = super().clean()
        from_time = cleaned_data.get("from_time")
        to_time = cleaned_data.get("to_time")

        if from_time and to_time and from_time > to_time:
            raise forms.ValidationError("End time must be greater than start time")
        return cleaned_data
