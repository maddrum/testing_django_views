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
        form_data["to_time"] = "00:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_to_midnight(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "10:00"
        form_data["to_time"] = "00:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_valid_non_stop(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "00:00"
        form_data["to_time"] = "00:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

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
        form_data["from_time"] = "24:00"
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

    def test_note_is_not_required(self):
        form_data = self.form_data.copy()
        form_data["note"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        del form_data["note"]
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

