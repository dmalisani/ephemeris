from django.test import TestCase
from eph_calendar.models import RegisteredDate
from django.contrib.auth.models import User
from datetime import date
from eph_calendar.viewsets import DatesViewSet


class TestModel(TestCase):

    def setUp(self):
        user = User.objects.create(username="tester")
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=7, day=15),
            title="test_day1"
        )

    def test_set_data_ok(self):
        expected_date = date(year=2020, month=7, day=15)
        self.assertEqual(self.new_record.date, expected_date, "Bad date registered")
        self.assertEqual(self.new_record.title, "test_day1", "Bad title registration")


class TestDateValidation(TestCase):
    def test_date_validation_ok(self):
        self.assertEqual(
            DatesViewSet._valid_date("2020-07-31"),
            date(year=2020, month=7, day=31),
            "Wrong date validation"
        )
        self.assertEqual(
            DatesViewSet._valid_date("2020-7-1"),
            date(year=2020, month=7, day=1),
            "Wrong date validation"
        )

    def test_date_validation_not_ok(self):
        self.assertIsNone(
            DatesViewSet._valid_date("2020-07-32"),
            "Wrong date validation"
        )
        self.assertIsNone(
            DatesViewSet._valid_date("any-string"),
            "Wrong date validation"
        )
        self.assertIsNone(
            DatesViewSet._valid_date("1-3-2020"),
            "Wrong date validation"
        )

