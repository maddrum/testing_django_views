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

    def _adjust_midnight(self) -> None:
        """

        Adjusts the `to_time` field to handle midnight user input cases.

        If the user inputs 24:00(:00)..., this method will convert it to 00:00,
        as that is handled on model level.

        Cases where user inputs something like `24:00`
        are NOT valid in from `datetime.time` perspective,
        but those ARE valid from human perspective.

        :return: None

        """

        if not bool(self.data.get("to_time")):
            return

        _value = self.data["to_time"].split(":")
        if len(_value) <= 1:
            return

        _all_other_are_zero = all(item == "00" for item in _value[1:])
        if not _all_other_are_zero:
            return

        if _value[0] != "24":
            return

        _value[0] = "00"
        self.data["to_time"] = ":".join(_value)

    def full_clean(self):
        self._adjust_midnight()
        super().full_clean()

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
            raise forms.ValidationError("End time must be greater than start time")

        # make sure minimal working hours are met
        if total_duration < MIN_WORKING_TIME_DURATION_HOURS and to_time != datetime.time(0, 0):
            raise forms.ValidationError(f"Total duration should be at least {MIN_WORKING_TIME_DURATION_HOURS} hour")

        return cleaned_data
