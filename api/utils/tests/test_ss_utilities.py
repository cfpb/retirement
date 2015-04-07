import os
import sys
import json
import datetime
today = datetime.datetime.now().date()

import mock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# if __name__ == "__main__" and __package__ is None:
#     __package__ = "utils.tests.test_ss_utilities"

from django.test import TestCase

from ..ss_utilities import get_retirement_age, get_delay_bonus, yob_test, age_map
from ..ss_calculator import get_retire_data, num_test, parse_details, requests
# from mock import Mock, patch

class UtilitiesTests(TestCase):
    sample_params = {
        'dobmon': 8,
        'dobday': 14,
        'yob': 1956,
        'earnings': 50000,
        'lastYearEarn': '',# possible use for unemployed or already retired
        'lastEarn': '',# possible use for unemployed or already retired
        'retiremonth': '',# leve blank to get triple calculation -- 62, 67 and 70
        'retireyear': '',# leve blank to get triple calculation -- 62, 67 and 70
        'dollars': 1,# benefits to be calculated in current-year dollars
        'prgf': 2
    }

    def test_parse_details(self):
        sample_rows = [
            "early: Base year for indexing is 2013.  Bend points are 826 & 4980",
            "AIME = 2930 & PIA in 2018 is 1416.6.",
            "PIA in 2018 after COLAs is $1,416.60."
        ]
        output = {'EARLY': {'AIME': 'AIME = 2930 & PIA in 2018 is 1416.6.', 'Bend points': 'Base year for indexing is 2013.  Bend points are 826 & 4980', 'COLA': 'PIA in 2018 after COLAs is $1,416.60.'}}
        self.assertEqual(parse_details(sample_rows), output)

    def test_num_test(self):
        inputs = [
            ("",     False),
            ("a",    False),
            ("3c",   False),
            ("4",    True),
            (4,      True),
            (4.4,    True),
            ("55.0", True),
            ("0.55", True)
        ]
        for tup in inputs:
            self.assertEqual(num_test(tup[0]), tup[1])

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
            "1922": None,
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

    def test_ss_calculator(self):
        """ given a birth date and annual pay value,
        return a dictionary of social security values
        """
        data_keys = [u'benefits', u'params', u'earnings_data', u'benefit_details']
        benefit_keys = [u'62 and 1 month in 2018', u'70 in 2026', u'66 and 4 months in 2022']
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['params']['yob'], 1956)
        for each in data.keys():
            self.assertTrue(each in data_keys)    
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)    
        self.sample_params['retiremonth'] = 6
        self.sample_params['retireyear'] = 2025
        data2 = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(isinstance(data2, dict))
        self.assertEqual(data2['params']['yob'], 1956)
        for each in data.keys():
            self.assertTrue(each in data_keys)    
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)    

    @mock.patch('requests.post')
    def test_ss_calculator_bad_request(self, mock_requests):
        mock_requests.return_value.reason = 'Not found'
        results = get_retire_data(self.sample_params)
        self.assertEqual(results['benefits'], {})


        