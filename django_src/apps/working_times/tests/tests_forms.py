import datetime

from django.test import TestCase

from ..forms import WorkingTimeForm


class WorkingTimeFormTests(TestCase):
    def setUp(self):
        self.form_data = {
            "client_name": "Test Client",
            "from_time": "12:00",
            "to_time": "18:00",
            "note": "Test note",
        }

    def expand_datetime(self, time):
        return datetime.datetime.combine(datetime.date.today(), time)

    def test_valid(self):
        form = WorkingTimeForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_valid_to_midnight(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "10:00"
        form_data["to_time"] = "00:00"
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_from_and_to_time(self):
        _form_data = self.form_data.copy()
        _form_data["from_time"] = "24:00"
        form = WorkingTimeForm(data=_form_data)
        self.assertFalse(form.is_valid())

        _form_data = self.form_data.copy()
        _form_data["to_time"] = "24:00"
        form = WorkingTimeForm(data=_form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_start_time_greater_than_end_time(self):
        form_data = self.form_data.copy()
        form_data["from_time"] = "19:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("End time must be greater than start time", form.errors["__all__"])

        form_data = self.form_data.copy()
        form_data["from_time"] = "18:00"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("End time must be greater than start time", form.errors["__all__"])

        form_data = self.form_data.copy()
        form_data["to_time"] = "00:00"
        form_data["from_time"] = "23:59"
        form = WorkingTimeForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_total_duration_should_be_more_than_min_hours(self):
        # TODO
        pass

    def test_note_is_not_required(self):
        form_data = self.form_data.copy()
        form_data["note"] = ""
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid())

        del form_data["note"]
        form = WorkingTimeForm(data=form_data)
        self.assertTrue(form.is_valid())
