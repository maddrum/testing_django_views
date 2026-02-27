import datetime

from django.db import models

from apps.working_times.settings import REPRESENTATION_TIME_FORMAT


class WorkingTime(models.Model):
    client_name = models.CharField(max_length=100)
    from_time = models.TimeField()
    to_time = models.TimeField()
    note = models.CharField(max_length=255, blank=True)

    TIME_FORMAT = "%H:%M"

    def __str__(self):
        return f"{self.from_time} - {self.to_time}"

    @property
    def time_of_day(self) -> str:
        """
        Returns the time of day.

        :return: The time of day, either "Morning" or "Afternoon".
        :rtype: str
        """
        if self.from_time.hour < 12:
            return "Morning"
        else:
            return "Afternoon"

    @property
    def readable_time(self) -> str:
        """
        Returns the readable time.

        :return: The readable time.
        :rtype: str
        """
        if self.to_time == datetime.time(0, 0):
            if self.from_time == datetime.time(0, 0):
                return "Non-stop"
            else:
                return f"{self.from_time.strftime('%H:%M')} - midnight"

        return (
            f"{self.from_time.strftime(REPRESENTATION_TIME_FORMAT)} - "
            f"{self.to_time.strftime(REPRESENTATION_TIME_FORMAT)}"
        )
