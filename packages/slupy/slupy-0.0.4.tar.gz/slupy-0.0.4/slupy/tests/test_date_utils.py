from datetime import date, datetime, timezone
import unittest

from slupy.dates import functions, utils


class TestDateUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.datetime_obj: datetime = datetime(
            year=2020,
            month=5,
            day=25,
            hour=17,
            minute=30,
            second=0,
            tzinfo=timezone.utc,
        )
        self.date_obj_1: date = date(year=2019, month=2, day=25)  # month with 28 days
        self.date_obj_2: date = date(year=2020, month=2, day=25)  # month with 29 days
        self.date_obj_3: date = date(year=2020, month=12, day=25)  # month with 31 days
        self.date_obj_4: date = date(year=2020, month=4, day=25)  # month with 30 days

    def test_is_first_day_of_month(self):
        self.assertTrue(
            utils.is_first_day_of_month(date(year=2019, month=2, day=1)),
        )
        self.assertTrue(
            not utils.is_first_day_of_month(date(year=2019, month=2, day=2)),
        )

    def test_is_last_day_of_month(self):
        self.assertTrue(
            utils.is_last_day_of_month(date(year=2019, month=2, day=28)),
        )
        self.assertTrue(
            utils.is_last_day_of_month(date(year=2020, month=2, day=29)),
        )
        self.assertTrue(
            not utils.is_last_day_of_month(date(year=2020, month=2, day=28)),
        )
        self.assertTrue(
            utils.is_last_day_of_month(date(year=2020, month=6, day=30)),
        )
        self.assertTrue(
            not utils.is_last_day_of_month(date(year=2020, month=12, day=30)),
        )
        self.assertTrue(
            utils.is_last_day_of_month(date(year=2020, month=12, day=31)),
        )

    def test_is_first_day_of_year(self):
        self.assertTrue(
            utils.is_first_day_of_year(date(year=2019, month=1, day=1)),
        )
        self.assertTrue(
            not utils.is_first_day_of_year(date(year=2019, month=1, day=2)),
        )

    def test_is_last_day_of_year(self):
        self.assertTrue(
            utils.is_last_day_of_year(date(year=2019, month=12, day=31)),
        )
        self.assertTrue(
            not utils.is_last_day_of_year(date(year=2019, month=12, day=30)),
        )

    def test_get_first_day_of_current_month(self):
        self.assertEqual(
            utils.get_first_day_of_current_month(self.date_obj_1),
            date(year=2019, month=2, day=1),
        )

    def test_get_last_day_of_current_month(self):
        self.assertEqual(
            utils.get_last_day_of_current_month(self.date_obj_1),
            date(year=2019, month=2, day=28),
        )
        self.assertEqual(
            utils.get_last_day_of_current_month(self.date_obj_2),
            date(year=2020, month=2, day=29),
        )
        self.assertEqual(
            utils.get_last_day_of_current_month(self.date_obj_3),
            date(year=2020, month=12, day=31),
        )
        self.assertEqual(
            utils.get_last_day_of_current_month(self.date_obj_4),
            date(year=2020, month=4, day=30),
        )

    def test_get_first_day_of_next_month(self):        
        self.assertEqual(
            utils.get_first_day_of_next_month(self.date_obj_3),
            date(year=2021, month=1, day=1),
        )

    def test_is_february_29th(self):
        self.assertTrue(
            utils.is_february_29th(date(year=2020, month=2, day=29)),
        )
        self.assertTrue(
            not utils.is_february_29th(date(year=2020, month=2, day=28)),
        )

    def test_compare_day_and_month(self):
        self.assertEqual(
            utils.compare_day_and_month(
                date(year=2020, month=1, day=25),
                date(year=2016, month=3, day=16),
            ),
            "<",
        )
        self.assertEqual(
            utils.compare_day_and_month(
                date(year=2016, month=3, day=16),
                date(year=2020, month=1, day=25),
            ),
            ">",
        )
        self.assertEqual(
            utils.compare_day_and_month(
                date(year=2016, month=4, day=20),
                date(year=2020, month=4, day=20),
            ),
            "==",
        )

    def test_compute_date_difference(self):
        self.assertEqual(
            utils.compute_date_difference(
                date(year=2020, month=1, day=11),
                date(year=2020, month=6, day=28),
            ),
            (0, 169),
        )
        self.assertEqual(
            utils.compute_date_difference(
                date(year=2019, month=1, day=11),
                date(year=2020, month=6, day=28),
            ),
            (1, 169),
        )
        self.assertEqual(
            utils.compute_date_difference(
                date(year=2019, month=1, day=11),
                date(year=2021, month=6, day=28),
            ),
            (2, 168),
        )

    def test_is_leap_year(self):
        self.assertTrue(
            utils.is_leap_year(2000),
        )
        self.assertTrue(
            not utils.is_leap_year(2001),
        )
        self.assertTrue(
            not utils.is_leap_year(2010),
        )
        self.assertTrue(
            not utils.is_leap_year(2100),
        )

    def test_get_day_of_week(self):
        self.assertEqual(
            utils.get_day_of_week(date(year=1996, month=6, day=28), shorten=False),
            "Friday",
        )
        self.assertEqual(
            utils.get_day_of_week(date(year=1996, month=6, day=28), shorten=True),
            "Fri",
        )

    def test_offset_between_datetimes(self):
        self.assertEqual(
            functions.offset_between_datetimes(
                start=date(year=2000, month=1, day=21),
                end=date(year=2000, month=1, day=27),
                offset_kwargs=dict(days=1),
                ascending=True,
                as_string=True,
            ),
            [
                "2000-01-21",
                "2000-01-22",
                "2000-01-23",
                "2000-01-24",
                "2000-01-25",
                "2000-01-26",
                "2000-01-27",
            ],
        )

    def test_get_datetime_buckets(self):
        self.assertEqual(
            functions.get_datetime_buckets(
                start=date(year=2000, month=1, day=1),
                num_buckets=5,
                offset_kwargs=dict(weeks=1),
                ascending=True,
                as_string=True,
            ),
            [
                ("2000-01-01", "2000-01-07"),
                ("2000-01-08", "2000-01-14"),
                ("2000-01-15", "2000-01-21"),
                ("2000-01-22", "2000-01-28"),
                ("2000-01-29", "2000-02-04"),
            ],
        )

        self.assertEqual(
            functions.get_datetime_buckets(
                start=date(year=2000, month=1, day=1),
                num_buckets=5,
                offset_kwargs=dict(weeks=1),
                ascending=False,
                as_string=True,
            ),
            [
                ('1999-11-28', '1999-12-04'),
                ('1999-12-05', '1999-12-11'),
                ('1999-12-12', '1999-12-18'),
                ('1999-12-19', '1999-12-25'),
                ('1999-12-26', '2000-01-01'),
            ],
        )


