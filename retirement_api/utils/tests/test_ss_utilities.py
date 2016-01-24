import os
import sys
import json
import datetime
from datetime import timedelta

import requests
import mock
import unittest

from ..ss_utilities import get_delay_bonus, get_months_past_birthday, yob_test
from ..ss_utilities import get_retirement_age, get_months_until_next_birthday
from ..ss_utilities import past_fra_test, get_current_age, age_map
from ..ss_calculator import num_test, parse_details
from ..ss_calculator import interpolate_benefits, get_retire_data
from ..check_api import TimeoutError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# from ...utils import ss_update_stats
# from retirement_api import utils


class UtilitiesTests(unittest.TestCase):
    today = datetime.date.today()
    sample_params = {
        'dobmon': 1,
        'dobday': 1,
        'yob': 1970,
        'earnings': 70000,
        'lastYearEarn': '',
        'lastEarn': '',
        'retiremonth': '{0}'.format(today.month),
        'retireyear': '{0}'.format(today.year),
        'dollars': 1,
        'prgf': 2
    }

    def test_months_past_birthday(self):
        dob = self.today-timedelta(days=365*20)
        self.assertTrue(get_months_past_birthday(dob) == 0)
        dob = self.today-timedelta(days=(365*20)+70)
        self.assertTrue(get_months_past_birthday(dob) == 2)
        dob = self.today-timedelta(days=(365*20)+320)
        self.assertTrue(get_months_past_birthday(dob) == 10)

    def test_months_until_next_bday(self):
        age40 = self.today.replace(year=(self.today.year - 40))
        bd_one_day_later = age40 + datetime.timedelta(days=1)
        bd_month_later = age40 + datetime.timedelta(days=30)
        diff1 = get_months_until_next_birthday(age40)
        diff2 = get_months_until_next_birthday(bd_one_day_later)
        diff3 = get_months_until_next_birthday(bd_month_later)
        self.assertTrue(diff1 == 12)
        self.assertTrue(diff2 in [0, 1])
        self.assertTrue(diff3 in [1, 2])

    def test_get_current_age(self):
        age_pairs = [(self.today.replace(year=self.today.year - 1), 1),
                     ('{}'.format(self.today.replace(year=self.today.year - 1)), 1),
                     (self.today.replace(year=self.today.year - 20), 20),
                     (self.today.replace(year=self.today.year - 60), 60),
                     (self.today, None),
                     ('xx', None),
                     (self.today + datetime.timedelta(days=1), None)]
        for pair in age_pairs:
            self.assertEqual(get_current_age(pair[0]), pair[1])

    def test_interpolate_benefits(self):
        mock_results = {'data': {'early retirement age': '',
                                 'full retirement age': '',
                                 'benefits': {'age 62': 0,
                                              'age 63': 0,
                                              'age 64': 0,
                                              'age 65': 0,
                                              'age 66': 0,
                                              'age 67': 2261,
                                              'age 68': 0,
                                              'age 69': 0,
                                              'age 70': 0,
                                              },
                                 'params': self.sample_params,
                                 'disability': '',
                                 'survivor benefits': {
                                        'child': '',
                                        'spouse caring for child': '',
                                        'spouse at full retirement age': '',
                                        'family maximum': ''
                                        }
                                 },
                        'current_age': 0,
                        'error': '',
                        'note': '',
                        'past_fra': False,
                        }
        benefits = {
            'age 62': 1602,
            'age 63': 1696,
            'age 64': 1809,
            'age 65': 1960,
            'age 66': 2110,
            'age 67': 2261,
            'age 68': 2442,
            'age 69': 2623,
            'age 70': 2804,
            }
        dob = self.today - datetime.timedelta(days=365*44)
        # results, base, fra_tuple, current_age, DOB
        results = interpolate_benefits(mock_results, 2261, (67, 0), 44, dob)
        for key in results['data']['benefits'].keys():
            self.assertEqual(results['data']['benefits'][key], benefits[key])
        mock_results['data']['benefits']['age 66'] = mock_results['data']['benefits']['age 67']
        mock_results['data']['benefits']['age 67'] = 0
        dob = self.today - datetime.timedelta(days=365*55)
        results = interpolate_benefits(mock_results, 2261, (66, 0), 55, dob)
        for key in sorted(results['data']['benefits'].keys()):
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = self.today - datetime.timedelta(days=365*64)
        results = interpolate_benefits(mock_results, 2261, (66, 0), 64, dob)
        for key in sorted(results['data']['benefits'].keys())[2:]:
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = self.today - datetime.timedelta(days=365*65)
        results = interpolate_benefits(mock_results, 2261, (66, 0), 65, dob)
        for key in sorted(results['data']['benefits'].keys())[3:]:
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = self.today - datetime.timedelta(days=365*63)
        results = interpolate_benefits(mock_results, 2261, (66, 0), 63, dob)
        for key in sorted(results['data']['benefits'].keys())[1:]:
            self.assertTrue(results['data']['benefits'][key] != 0)

    def test_parse_details(self):
        sample_rows = [
           "early: Base year for indexing is 2013. Bend points are 826 & 4980",
           "AIME = 2930 & PIA in 2018 is 1416.6.",
           "PIA in 2018 after COLAs is $1,416.60."
           ]
        output = {'EARLY':
                  {'AIME': 'AIME = 2930 & PIA in 2018 is 1416.6.',
                   'Bend points': 'Base year for indexing is 2013. Bend points are 826 & 4980',
                   'COLA': 'PIA in 2018 after COLAs is $1,416.60.'}}
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
        """
        given a worker's birth year,
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
            str(self.today.year+1): None,
        }
        for year in sample_inputs:
            self.assertEqual(get_retirement_age(year), sample_inputs[year])

    def test_past_fra_test(self):
        way_old = "%s" % (self.today-timedelta(days=80*365))
        too_old = "%s" % (self.today-timedelta(days=68*365))
        ok = "%s" % (self.today-timedelta(days=57*365))
        too_young = "%s" % (self.today-timedelta(days=21*365))
        future = "%s" % (self.today+timedelta(days=365))
        edge = "%s" % (self.today-timedelta(days=67*365))
        invalid = "xx/xx/xxxx"
        self.assertTrue(past_fra_test(too_old, language='en') == True)
        self.assertTrue(past_fra_test(too_old, language='es') == True)
        self.assertTrue(past_fra_test(ok, language='en') == False)
        self.assertTrue("22" in past_fra_test(too_young, language='en'))
        self.assertTrue("sentimos" in past_fra_test(too_young, language='es'))
        self.assertTrue("invalid birth" in past_fra_test(future, language='en'))
        self.assertTrue("70" in past_fra_test(way_old, language='en'))
        self.assertTrue(past_fra_test(edge, language='en') == True)
        self.assertTrue("invalid" in past_fra_test(invalid, language='en'))
        self.assertTrue("invalid" in past_fra_test())

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
            str(self.today.year+2): None,
            "935": None,
            "1957": "1957",
            "1979": "1979",
            "abc": None,
            1980: "1980",
            None: None
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

    def test_get_retire_data(self):
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
        data = get_retire_data(self.sample_params, language='en')['data']
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['params']['yob'], 1970)
        for each in data.keys():
            self.assertTrue(each in data_keys)
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)
        self.sample_params['yob'] = 1937
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['data']['params']['yob'], 1937)
        self.assertTrue('70' in data['note'])
        self.sample_params['yob'] = self.today.year-21
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue("22" in data['note'])
        self.sample_params['yob'] = self.today.year-57
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 62'] != 0)
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-64
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-65
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-66
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.assertTrue(data['data']['benefits']['age 66'] != 0)
        self.sample_params['yob'] = self.today.year-67
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-68
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-69
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = self.today.year-70
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['earnings'] = 0
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue("zero" in data['error'])
        self.sample_params['yob'] = self.today.year-45
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue("zero" in data['error'] or "SSA" in data['error'])
        self.sample_params['earnings'] = 100000
        self.sample_params['yob'] = self.today.year-68
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue("past" in data['note'])
        self.sample_params['yob'] = self.today.year + 1
        data = get_retire_data(self.sample_params, language='en')
        self.assertTrue("invalid" in data['note'])

    @mock.patch('retirement_api.utils.ss_calculator.requests.post')
    def test_bad_calculator_requests(self, mock_requests):
        mock_requests.return_value.ok = False
        mock_results = get_retire_data(self.sample_params, language='en')
        self.assertTrue('not responding' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.RequestException
        mock_results = get_retire_data(self.sample_params, language='en')
        self.assertTrue('request error' in mock_results['error'])
        mock_results = get_retire_data(self.sample_params, language='es')
        self.assertTrue('request error' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.ConnectionError
        mock_results = get_retire_data(self.sample_params, language='en')
        self.assertTrue('connection error' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.Timeout
        mock_results = get_retire_data(self.sample_params, language='en')
        self.assertTrue('timed out' in mock_results['error'])
        mock_requests.side_effect = ValueError
        mock_results = get_retire_data(self.sample_params, language='en')
        self.assertTrue('SSA' in mock_results['error'])
