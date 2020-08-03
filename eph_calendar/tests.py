from django.test import TestCase
from eph_calendar.models import RegisteredDate
from django.contrib.auth.models import User
from datetime import date
from eph_calendar.viewsets import DatesViewSet
from django.test import Client
import json


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


class TestVieset(TestCase):
    def setUp(self):
        """Makes two entries in same day, twice on july, twice in august."""
        user = User.objects.create(username="tester")
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=7, day=15),
            title="test_day15_1"
        )
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=7, day=15),
            title="test_day15_2"
        )
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=7, day=20),
            title="test_day20_1"
        )
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=7, day=20),
            title="test_day20_2"
        )
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=8, day=20),
            title="test_day20_1"
        )
        self.new_record = RegisteredDate.objects.create(
            registered_by=user,
            date=date(year=2020, month=8, day=20),
            title="test_day20_2"
        )

    def test_preconditions(self):
        self.assertEqual(
            len(RegisteredDate.objects.all()),
            6,
            "You added not whatched dates"
        )
        self.assertEqual(
            len(RegisteredDate.objects.filter(
                date__day=20,
                date__month=7,
                date__year=2020)),
            2,
            "You added not whatched dates on july 20"
        )
        self.assertEqual(
            len(RegisteredDate.objects.filter(
                date__month=7,
                date__year=2020)),
            4,
            "You added not whatched dates on july"
        )

    def test_integration_bad_request(self):
        cli = Client()
        response = cli.get('/efemerides/?dia=no_valid_date')
        self.assertEqual(response.status_code, 400)

    def test_integration_empty_response(self):
        cli = Client()
        response = cli.get('/efemerides/?dia=2020-09-01')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,  {'hoy': [], 'mes': {}})

    def test_integration_response_july_20(self):
        cli = Client()
        response = cli.get('/efemerides/?dia=2020-07-20')
        expected_response = {
            'hoy': ['test_day20_1', 'test_day20_2'],
            'mes': {'15': ['test_day15_1', 'test_day15_2'],
                    '20': ['test_day20_1', 'test_day20_2']}}

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,  expected_response)

    def test_integration_response_august_20(self):
        cli = Client()
        response = cli.get('/efemerides/?dia=2020-08-1')
        expected_response = {
            'hoy': [], 'mes': {'20': ['test_day20_1', 'test_day20_2']}
        }
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,  expected_response)
