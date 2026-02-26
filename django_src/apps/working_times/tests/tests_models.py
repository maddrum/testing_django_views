import datetime

from django.test import TestCase
from model_bakery import baker

from apps.working_times.models import WorkingTime


class WorkingTimeTests(TestCase):
    def test_time_of_day_morning(self):
        working_time = baker.make(
            WorkingTime,
            from_time=datetime.time(8, 0),
            to_time=datetime.time(12, 0),
        )
        self.assertEqual("Morning", working_time.time_of_day)

        working_time = baker.make(
            WorkingTime,
            from_time=datetime.time(11, 59),
            to_time=datetime.time(12, 0),
        )
        self.assertEqual("Morning", working_time.time_of_day)

    def test_time_of_day_afternoon(self):
        working_time = baker.make(
            WorkingTime,
            from_time=datetime.time(12, 0),
            to_time=datetime.time(18, 0),
        )
        self.assertEqual("Afternoon", working_time.time_of_day)

        working_time = baker.make(
            WorkingTime,
            from_time=datetime.time(14, 0),
            to_time=datetime.time(18, 0),
        )
        self.assertEqual("Afternoon", working_time.time_of_day)

    def test_str(self):
        working_time = baker.make(
            WorkingTime,
            from_time=datetime.time(8, 0),
            to_time=datetime.time(12, 0),
        )
        self.assertEqual("08:00:00 - 12:00:00", str(working_time))
