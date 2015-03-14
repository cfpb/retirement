import os
import sys
import json
import datetime
today = datetime.datetime.now().date()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.test import TestCase
from .ss_utilities import get_retirement_age, get_delay_bonus, yob_test, age_map
# from mock import Mock, patch

class UtilitiesTests(TestCase):

    def test_get_retirement_age(self):
        """ given a worker's birth year, 
            should return full retirement age in years and months
        """
        sample_inputs = {
            "1920": (65, 0),
            "1937": (65, 0),
            "1938": (65, 2),
            "1939": (65, 4),
            "1940": (65, 6),
            "1941": (65, 8),
            "1942": (65, 10),
            "1943": (66, 0),
            "1945": (66, 0),
            "1954": (66, 0),
            "1955": (66, 2),
            "1956": (66, 4),
            "1957": (66, 6),
            "1958": (66, 8),
            "1959": (66, 10),
            "1960": (67, 0),
            "1980": (67, 0),
            '198': None,
            'abc': None,
            str(today.year+1): None,
        }
        for year in sample_inputs:
            self.assertEqual(get_retirement_age(year), sample_inputs[year])

    def test_age_map(self):
        self.assertTrue(isinstance(age_map, dict))
        for year in age_map:
            self.assertTrue(isinstance(age_map[year], tuple))

    def test_get_delay_bonus(self):
        sample_inputs = {
            "1933": 5.5,
            "1934": 5.5,
            "1935": 6.0,
            "1937": 6.5,
            "1939": 7.0,
            "1941": 7.5,
            "1943": 8.0,
            "1953": 8.0,
            "1963": 8.0,
            "1973": 8.0,
            "1983": 8.0,
        }
        for year in sample_inputs:
            self.assertEqual(get_delay_bonus(year), sample_inputs[year])

    def test_yob_test(self):
        sample_inputs = {
            "1933": "1933",
            str(today.year+2): None,
            "935": None,
            "1957": "1957",
            "1979": "1979",
            "abc": None,
            1980: "1980"
        }
        for year in sample_inputs:
            self.assertEqual(yob_test(year), sample_inputs[year])

        