from django.db import models


class WorkingTime(models.Model):
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return f"{self.from_time} - {self.to_time}"

    @property
    def time_of_day(self) -> str:
        """
        Get the time of day the working time falls in.

        Returns:
            str: The time of day the working time falls in. Possible values are "Morning" or "Afternoon".
        """

        if self.from_time.hour < 12:
            return "Morning"
        else:
            return "Afternoon"
