import datetime

from django import forms

from .models import WorkingTime
from .settings import MIN_WORKING_TIME_DURATION_HOURS


class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = ["from_time", "to_time"]

    def _expand_to_datetime(self, time: datetime.time) -> datetime.datetime:
        return datetime.datetime.combine(datetime.date.today(), time)

    def clean(self):
        cleaned_data = super().clean()
        _from_time = cleaned_data.get("from_time")
        _to_time = cleaned_data.get("to_time")

        if not _from_time or not _to_time:
            return cleaned_data

        from_time = self._expand_to_datetime(_from_time)
        to_time = self._expand_to_datetime(_to_time)
        total_duration = (to_time - from_time).total_seconds() / 3600

        if from_time > to_time:
            raise forms.ValidationError("End time must be greater than start time")

        if total_duration < MIN_WORKING_TIME_DURATION_HOURS:
            raise forms.ValidationError(f"Total duration should be at least {MIN_WORKING_TIME_DURATION_HOURS} hour")

        return cleaned_data
