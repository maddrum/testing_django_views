import datetime

from django import forms

from .models import WorkingTime
from .settings import MIN_WORKING_TIME_DURATION_HOURS


class WorkingTimeForm(forms.ModelForm):
    class Meta:
        model = WorkingTime
        fields = ["from_time", "to_time"]

    @staticmethod
    def _expand_to_datetime(time: datetime.time) -> datetime.datetime:
        """
        Expand a time to a datetime.

        :param time: Time to expand.
        :type time: datetime.time
        :return: Expanded datetime.
        :rtype: datetime.datetime
        """
        return datetime.datetime.combine(datetime.date.today(), time)

    def clean(self):
        cleaned_data = super().clean()
        _from_time = cleaned_data.get("from_time")
        _to_time = cleaned_data.get("to_time")

        # field was already dropped in field validation
        if not _from_time or not _to_time:
            return cleaned_data

        from_time = self._expand_to_datetime(_from_time)
        to_time = self._expand_to_datetime(_to_time)
        total_duration = (to_time - from_time).total_seconds() / 3600

        # make sure to time is greater than from time
        if to_time <= from_time:
            raise forms.ValidationError("End time must be greater than start time")

        # make sure minimal working hours are met
        if total_duration < MIN_WORKING_TIME_DURATION_HOURS:
            raise forms.ValidationError(f"Total duration should be at least {MIN_WORKING_TIME_DURATION_HOURS} hour")

        return cleaned_data
