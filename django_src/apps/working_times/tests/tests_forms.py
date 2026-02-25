from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from ..forms import WorkingTimeForm


class WorkingTimeFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "from_time": "12:00",
            "to_time": "18:00",
        }

    def test_working_time_form_valid(self):
        form = WorkingTimeForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_working_time_form_invalid_start_time_greater_than_end_time(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "18:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("End time must be greater than start time", form.errors["__all__"])

    def test_working_time_form_invalid_start_time_and_end_time_empty(self):
        pass
