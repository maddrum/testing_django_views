import logging

from django.test import TestCase

from apps.working_times.forms import WorkingTimeForm

logger = logging.getLogger("app")


class WorkingTimeFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "shop_name": "Dunki 2k",
            "from_time": "10:00",
            "to_time": "18:00",
            "note": "Sometimes is closed for no reason",
        }

    def test_valid(self):
        form = WorkingTimeForm(data=self.form_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_missing_shop_name(self):
        form_data = self.form_data.copy()
        form_data["shop_name"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["shop_name"])

        form_data = self.form_data.copy()
        del form_data["shop_name"]
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["shop_name"])

    def test_invalid_missing_to_time(self):
        form_data = self.form_data.copy()
        form_data["to_time"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["to_time"])

        form_data = self.form_data.copy()
        del form_data["to_time"]
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["to_time"])

    def test_invalid_missing_from_time(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["from_time"])

        form_data = self.form_data.copy()
        del form_data["from_time"]
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["from_time"])

    def test_invalid_from_time_should_be_at_least_07_00(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "06:59"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Minimum allowed opening time is 07:00", form.errors["from_time"])

    def test_invalid_to_time_should_be_max_22_00(self):
        form_data = self.form_data.copy()
        form_data["to_time"] = "22:01"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Maximum allowed closing time is 22:00", form.errors["to_time"])

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
