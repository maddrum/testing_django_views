import datetime
import logging

from django.test import TestCase

from apps.working_times.forms import WorkingTimeForm
from apps.working_times.settings import MIN_WORKING_TIME_DURATION_HOURS, REPRESENTATION_TIME_FORMAT

logger = logging.getLogger("app")


class WorkingTimeFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "client_name": "Test Client",
            "from_time": "10:00",
            "to_time": "18:00",
            "note": "Test note",
        }

    def test_valid(self):
        form = WorkingTimeForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_edge_cases(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "00:00"
        form_data["to_time"] = "10:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["from_time"] = "00:00"
        form_data["to_time"] = "10:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["from_time"] = "10:00"
        form_data["to_time"] = "24:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["from_time"] = "00:00"
        form_data["to_time"] = "24:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_to_midnight(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "10:00"
        form_data["to_time"] = "24:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_non_stop(self):
        to_time = "24:00"
        for from_time in ["00:00", "24:00"]:
            logger.info("from_time: %s, to_time: %s", from_time, to_time)
            form_data = self.form_data.copy()
            form_data["from_time"] = from_time
            form_data["to_time"] = to_time
            form = WorkingTimeForm(data=form_data)
            self.assertTrue(form.is_valid(), form.errors)

    def test_valid_min_working_times(self):
        form_data = self.form_data.copy()
        to_time = datetime.datetime.combine(datetime.date.today(), datetime.time(18, 0))
        from_time = to_time - datetime.timedelta(hours=MIN_WORKING_TIME_DURATION_HOURS) - datetime.timedelta(minutes=1)
        form_data["to_time"] = to_time.strftime(REPRESENTATION_TIME_FORMAT)
        form_data["from_time"] = from_time.strftime(REPRESENTATION_TIME_FORMAT)
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data = self.form_data.copy()
        to_time = datetime.datetime.combine(datetime.date.today(), datetime.time(18, 0))
        from_time = to_time - datetime.timedelta(hours=MIN_WORKING_TIME_DURATION_HOURS)
        form_data["to_time"] = to_time.strftime(REPRESENTATION_TIME_FORMAT)
        form_data["from_time"] = from_time.strftime(REPRESENTATION_TIME_FORMAT)
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_missing_to_time(self):
        form_data = self.form_data.copy()
        form_data["to_time"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        del form_data["to_time"]
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_from_and_to_time(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "24:01"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["from_time"] = "not time"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["to_time"] = "24:01"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

        form_data = self.form_data.copy()
        form_data["to_time"] = "not time"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_invalid_to_time_can_not_be_00_00(self):
        form_data = self.form_data.copy()
        form_data["to_time"] = "00:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("To time must be greater than 00:00", form.errors["to_time"])

    def test_invalid_start_time_greater_than_end_time(self):
        error_message = "End time must be greater than start time"

        form_data = self.form_data.copy()
        form_data["from_time"] = "19:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(error_message, form.errors["__all__"], form.errors)

        form_data = self.form_data.copy()
        form_data["from_time"] = "18:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(error_message, form.errors["__all__"], form.errors)

    def test_invalid_total_duration_should_be_more_than_min_hours(self):
        error_message = f"Total duration should be at least {MIN_WORKING_TIME_DURATION_HOURS} hour"

        form_data = self.form_data.copy()
        to_time = datetime.datetime.combine(datetime.date.today(), datetime.time(18, 0))
        from_time = to_time - datetime.timedelta(hours=MIN_WORKING_TIME_DURATION_HOURS) + datetime.timedelta(minutes=1)
        form_data["to_time"] = to_time.strftime(REPRESENTATION_TIME_FORMAT)
        form_data["from_time"] = from_time.strftime(REPRESENTATION_TIME_FORMAT)
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(error_message, form.errors["__all__"], form.errors)

    def test_note_is_not_required(self):
        form_data = self.form_data.copy()
        form_data["note"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        del form_data["note"]
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_adjust_midnight(self):
        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        self.assertEqual({}, form.adjusted_midnight_initial)

        # Test case: 24:00 should be converted to 00:00
        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        form.data["to_time"] = "24:00"
        form._adjust_midnight("to_time")
        self.assertEqual("00:00", form.data["to_time"])
        self.assertEqual({"to_time": "24:00"}, form.adjusted_midnight_initial)

        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        form.data["from_time"] = "24:00:00"
        form._adjust_midnight("from_time")
        self.assertEqual("00:00:00", form.data["from_time"])
        self.assertEqual({"from_time": "24:00:00"}, form.adjusted_midnight_initial)

        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        form.data["to_time"] = "24:00"
        form.data["from_time"] = "24:00"
        form._adjust_midnight("from_time")
        form._adjust_midnight("to_time")
        self.assertEqual(form.data["from_time"], "00:00")
        self.assertEqual(form.data["to_time"], "00:00")
        self.assertEqual({"from_time": "24:00", "to_time": "24:00"}, form.adjusted_midnight_initial)

        # Test case: 23:59 should remain 23:59
        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        form.data["from_time"] = "23:59"
        form._adjust_midnight("from_time")
        self.assertEqual("23:59", form.data["from_time"])
        self.assertEqual({}, form.adjusted_midnight_initial)

        # Test case: 24:01 should remain 24:01 (invalid time, but _adjust_midnight shouldn't change it if not 24:00)
        form_data = self.form_data.copy()
        form = WorkingTimeForm(data=form_data)
        form.data["from_time"] = "24:01"
        form._adjust_midnight("from_time")
        self.assertEqual("24:01", form.data["from_time"])
        self.assertEqual({}, form.adjusted_midnight_initial)

        # Test case: Empty string
        form.data["from_time"] = ""
        form._adjust_midnight("from_time")
        self.assertEqual(
            "",
            form.data["from_time"],
        )
        self.assertEqual({}, form.adjusted_midnight_initial)

        # Test case: "24" (incomplete)
        form.data["from_time"] = "24"
        form._adjust_midnight("from_time")
        self.assertEqual(form.data["from_time"], "24")
        self.assertEqual({}, form.adjusted_midnight_initial)
