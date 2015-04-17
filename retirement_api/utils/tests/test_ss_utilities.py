import os
import sys
import json
import datetime
from datetime import timedelta
today = datetime.datetime.now().date()

import mock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# if __name__ == "__main__" and __package__ is None:
#     __package__ = "utils.tests.test_ss_utilities"

from django.test import TestCase

from ..ss_utilities import get_retirement_age, get_delay_bonus, yob_test, age_map, past_fra_test
from ..ss_calculator import get_retire_data, num_test, parse_details, requests, interpolate_benefits
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

    def test_interpolate_benefits(self):
        benefits = {
            'age 62': 1452,
            'age 63': 0,
            'age 64': 0,
            'age 65': 0,
            'age 66': 0,
            'age 67': 2113,
            'age 68': 0,
            'age 69': 0,
            'age 70': 2650,
            }
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys()):
            self.assertTrue(bens[key] != 0)
        benefits['age 66'] = benefits['age 67']
        benefits['age 67'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys()):
            self.assertTrue(bens[key] != 0)
        benefits['age 65'] = benefits['age 66']
        benefits['age 66'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys()):
            self.assertTrue(bens[key] != 0)
        benefits['age 62'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[3:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 66'] = benefits['age 65']
        benefits['age 65'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[4:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 67'] = benefits['age 66']
        benefits['age 66'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[5:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 68'] = benefits['age 67']
        benefits['age 67'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[6:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 69'] = benefits['age 68']
        benefits['age 68'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[7:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 66'] = benefits['age 69']
        benefits['age 65'] = 0
        benefits['age 64'] = 0
        benefits['age 63'] = 0
        benefits['age 62'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[4:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 67'] = benefits['age 66']
        benefits['age 66'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[5:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 68'] = benefits['age 67']
        benefits['age 67'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[6:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 69'] = benefits['age 68']
        benefits['age 68'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[7:]:
            self.assertTrue(bens[key] != 0)
        benefits['age 69'] = 0
        bens = interpolate_benefits(benefits)
        for key in sorted(bens.keys())[8:]:
            self.assertTrue(bens[key] != 0)


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

    def test_past_fra_test(self):
        way_old = "%s" % (today-timedelta(days=80*365))
        too_old = "%s" % (today-timedelta(days=68*365))
        ok = "%s" % (today-timedelta(days=57*365))
        too_young = "%s" % (today-timedelta(days=21*365))
        invalid = "%s" % (today+timedelta(days=365))
        edge = "%s" % (today-timedelta(days=67*365))
        self.assertTrue(past_fra_test(too_old) == True)
        self.assertTrue(past_fra_test(ok) == False)
        self.assertTrue(past_fra_test(too_young) == 'too young to calculate benefits')
        self.assertTrue(past_fra_test(invalid) == "invalid birth year")
        self.assertTrue(past_fra_test(way_old) == True)
        self.assertTrue(past_fra_test(edge) == False)

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

    """
    ## sample params: ##
            'dobmon': 8,
            'dobday': 14,
            'yob': 1956,
            'earnings': 50000,

    ## sample results: ##    
        results = {'data': {
                        'early retirement age': '', 
                        u'full retirement age': '', 
                        'benefits': {
                            'age 62': 0, 
                            'age 63': 0, 
                            'age 64': 0, 
                            'age 65': 0, 
                            'age 66': 0, 
                            'age 67': 0, 
                            'age 68': 0, 
                            'age 69': 0, 
                            'age 70': 0
                            }
                        'params': params,
                        'disability': '',
                        'survivor benefits': {
                                        'child': '',
                                        'spouse caring for child': '',
                                        'spouse at full retirement age': '',
                                        'family maximum': ''
                                        }
                        }
                  }
    """

    def test_ss_calculator(self):
        """ given a birth date and annual pay value,
        return a dictionary of social security values
        """
        data_keys = [u'early retirement age', 
                     u'full retirement age', 
                     u'benefits', 
                     u'params', 
                     u'disability',
                     u'survivor benefits']
        benefit_keys = ['age 62', 
                        'age 63', 
                        'age 64', 
                        'age 65', 
                        'age 66', 
                        'age 67', 
                        'age 68', 
                        'age 69', 
                        'age 70']
        data = json.loads(get_retire_data(self.sample_params))['data']
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['params']['yob'], 1956)
        for each in data.keys():
            self.assertTrue(each in data_keys)    
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)
        self.sample_params['yob'] = 1937
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['data']['params']['yob'], 1937)
        self.assertTrue('already past' in data['error'])

    @mock.patch('requests.post')
    def test_ss_calculator_bad_request(self, mock_requests):
        mock_requests.return_value.reason = 'Not found'
        results = json.loads(get_retire_data(self.sample_params))
        self.assertTrue('error' in results)


        