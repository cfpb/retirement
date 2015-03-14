import os
import sys
import json
import datetime
today = datetime.datetime.now().date()

import requests

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.test import TestCase
from .utils.update_ss_stats import update_life, update_cola, update_retirement_age
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

    def test_update_stats(self):
        """
        test scripts to update data tables 
        from Social Security

        """
        assertEqual(update_life(), True)
        assertEqual(update_cola(), True)
        assertEqual(update_retirement_age(), True)
