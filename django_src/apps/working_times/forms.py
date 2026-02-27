import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import WorkingTime


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
        from_time = cleaned_data.get("from_time")
        to_time = cleaned_data.get("to_time")

        # field was already dropped in field validation
        if not from_time or not to_time:
            return cleaned_data

        expanded_from_time = self._expand_to_datetime(from_time)
        expanded_to_time = self._expand_to_datetime(to_time)
        total_duration = (expanded_to_time - expanded_from_time).total_seconds() / 3600

        # make sure to time is greater than from time
        if expanded_to_time <= expanded_from_time and to_time != datetime.time(0, 0):
            raise ValidationError("End time must be greater than start time")

        return cleaned_data
