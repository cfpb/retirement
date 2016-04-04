import os
import sys
import json
import datetime
from copy import copy
from datetime import timedelta
from datetime import date

import requests
import mock
import unittest

import django
from retirement_api.models import Calibration
from retirement_api import utils

from ..ss_utilities import (get_retirement_age,
                            get_months_until_next_birthday,
                            past_fra_test,
                            get_current_age,
                            get_delay_bonus,
                            age_map,
                            get_months_past_birthday,
                            yob_test)
from ..ss_calculator import (num_test,
                             parse_details,
                             parse_response,
                             clean_comment,
                             interpolate_benefits,
                             interpolate_for_past_fra,
                             get_retire_data,
                             set_up_runvars)
from ..check_api import TimeoutError
from ..ssa_check import (TESTS, get_test_params, check_results, run_tests)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# from ...utils import ss_update_stats
# from retirement_api import utils


class SSACheckTests(django.test.TestCase):
    fixtures = ['test_calibration.json']
    sample_params = {
        'dobmon': 1,
        'dobday': 3,
        'yob': 1970,
        'earnings': 40000,
        'lastYearEarn': '',
        'lastEarn': '',
        'retiremonth': 1,
        'retireyear': 2037,
        'dollars': 1,
        'prgf': 2
    }

    def test_check_results(self):
        test_results = json.loads(Calibration.objects.first().results_json)
        test_data = test_results
        test_msg = check_results(test_data)
        self.assertTrue("pass" in test_msg)
        slug = test_results.keys()[0]
        test_data[slug]['current_age'] = 99
        test_data[slug]['current_age'] = 99
        test_data[slug]['data']['months_past_birthday'] = 13
        test_data[slug]['data']['benefits']['age 70'] = 0
        test_data[slug]['data']['params']['yob'] = 0
        test_msg2 = check_results(test_data)
        self.assertTrue("Mismatches" in test_msg2)

    @mock.patch('retirement_api.utils.ssa_check.get_retire_data')
    @mock.patch('retirement_api.utils.ssa_check.check_results')
    def test_run_tests(self, mock_check_results, mock_get_retire_data):
        mock_get_retire_data.return_value = Calibration.objects.first().results_json
        mock_check_results.return_value = "All pass"
        test1 = utils.ssa_check.run_tests()
        self.assertTrue(mock_get_retire_data.call_count == len(TESTS))
        self.assertTrue(mock_check_results.call_count == 1)
        self.assertTrue('pass' in test1)
        test2 = run_tests(recalibrate=True)
        self.assertTrue(Calibration.objects.count() == 2)


class UtilitiesTests(unittest.TestCase):
    today = datetime.date.today()
    if today.day == 29:  # in case this test runs in Feb. in a leap year
        today = today.replace(day=today.day - 1)
    sample_params = {
        'dobmon': 1,
        'dobday': 5,
        'yob': 1970,
        'earnings': 70000,
        'lastYearEarn': '',
        'lastEarn': '',
        'retiremonth': 1,
        'retireyear': 2037,
        'dollars': 1,
        'prgf': 2
    }

    def test_get_test_params(self):
        test_params = get_test_params(46, 3)
        self.assertTrue(test_params['dobday'] == 3)
        test_params = get_test_params(46, self.today.day + 1)
        self.assertTrue(test_params['dobday'] == self.today.day + 1)
        test_params = get_test_params(46, 3, dob_year=1950)
        self.assertTrue(test_params['yob'] == 1950)
        test_params = get_test_params(46, 3, dob_year=1950)
        self.assertTrue(test_params['yob'] == 1950)

    @mock.patch('retirement_api.utils.ssa_check.datetime.date')
    def test_get_test_params_jan(self, mock_date):
        mock_date.today.return_value = self.today.replace(month=1, day=2)
        test_params = get_test_params(46, 3)
        print "\n\n\nYOB OUTPUT IS {0}\n\n\n".format(test_params['yob'])
        self.assertTrue(test_params['yob'] == 1969)

    def test_clean_comment(self):
        test_comment = '<!-- This is a test comment    -->'
        expected_comment = 'This is a test comment'
        self.assertTrue(clean_comment(test_comment) == expected_comment)

    def test_set_up_runvars(self):
        mock_params = copy(self.sample_params)
        (test_dob,
         test_dobstring,
         test_current_age,
         test_fra_tuple,
         test_past_fra,
         test_results) = set_up_runvars(mock_params)
        self.assertTrue(test_results['data']['params']['yob'] == 1970)
        mock_params['dobday'] = 1
        (test_dob,
         test_dobstring,
         test_current_age,
         test_fra_tuple,
         test_past_fra,
         test_results2) = set_up_runvars(mock_params)
        self.assertTrue(test_results2['data']['params']['yob'] == 1969)

    def test_months_past_birthday(self):
        dob = self.today-timedelta(days=(365 * 20) + 6)
        self.assertTrue(get_months_past_birthday(dob) in [0, 1])
        dob = self.today-timedelta(days=(365 * 20) + 70)
        self.assertTrue(get_months_past_birthday(dob) in [2, 3])
        dob = self.today-timedelta(days=(365 * 20) + 320)
        self.assertTrue(get_months_past_birthday(dob) in [10, 11])

    def test_months_until_next_bday(self):
        age40 = self.today.replace(year=(self.today.year - 40))
        bd_two_days_later = age40 + datetime.timedelta(days=2)
        bd_month_later = age40 + datetime.timedelta(days=30)
        diff1 = get_months_until_next_birthday(age40)
        diff2 = get_months_until_next_birthday(bd_two_days_later)
        diff3 = get_months_until_next_birthday(bd_month_later)
        self.assertTrue(diff1 == 12)
        self.assertTrue(diff2 in [0, 1])
        self.assertTrue(diff3 in [1, 2])

    def test_get_current_age(self):
        age_pairs = [(self.today.replace(year=self.today.year - 1), 1),
                     ('{0}'.format(self.today.replace(year=self.today.year - 1)), 1),
                     (self.today.replace(year=self.today.year - 20), 20),
                     (self.today.replace(year=self.today.year - 60), 60),
                     (self.today, None),
                     ('xx', None),
                     (self.today + datetime.timedelta(days=2), None)]
        for pair in age_pairs:
            self.assertEqual(get_current_age(pair[0]), pair[1])

    @mock.patch('retirement_api.utils.ss_utilities.datetime.date')
    def test_get_current_age_leapyear(self, mock_date):
        mock_date.today.return_value = date(2015, 1, 29)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        age_pair = ('2-29-1980', 34)
        self.assertEqual(get_current_age(age_pair[0]), age_pair[1])

    def test_interpolate_benefits(self):
        params = copy(self.sample_params)
        mock_results = {'data': {'early retirement age': '',
                                 'full retirement age': '',
                                 'benefits': {'age 62': 0,
                                              'age 63': 0,
                                              'age 64': 0,
                                              'age 65': 0,
                                              'age 66': 0,
                                              'age 67': 2176,
                                              'age 68': 0,
                                              'age 69': 0,
                                              'age 70': 0,
                                              },
                                 'params': self.sample_params,
                                 'disability': '',
                                 'months_past_birthday': 0,
                                 'survivor benefits': {
                                        'child': '',
                                        'spouse caring for child': '',
                                        'spouse at full retirement age': '',
                                        'family maximum': ''
                                        }
                                 },
                        'current_age': 44,
                        'error': '',
                        'note': '',
                        'past_fra': False,
                        }
        benefits = {
            'age 62': 1532,
            'age 63': 1632,
            'age 64': 1741,
            'age 65': 1886,
            'age 66': 2031,
            'age 67': 2176,
            'age 68': 2350,
            'age 69': 2524,
            'age 70': 2698
            }
        dob = self.today - datetime.timedelta(days=365*44)
        # results, base, fra_tuple, current_age, DOB
        results = interpolate_benefits(mock_results, 2176, (67, 0), 44, dob)
        for key in results['data']['benefits'].keys():
            self.assertEqual(results['data']['benefits'][key], benefits[key])
        mock_results['data']['benefits']['age 66'] = mock_results['data']['benefits']['age 67'] 
        mock_results['data']['benefits']['age 67'] = 0
        dob = self.today - datetime.timedelta(days=365*55)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 55, dob)
        for key in sorted(results['data']['benefits'].keys()):
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = dob.replace(day=2)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 55, dob)
        self.assertTrue(results['data']['benefits']['age 62'] != 0)
        dob = dob.replace(year=self.today.year - 45)
        results = interpolate_benefits(mock_results, 2176, (67, 0), 45, dob)
        self.assertTrue(results['data']['benefits']['age 62'] != 0)
        dob = self.today - datetime.timedelta(days=365*64)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 64, dob)
        for key in sorted(results['data']['benefits'].keys())[2:]:
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = self.today - datetime.timedelta(days=365*65)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 65, dob)
        for key in sorted(results['data']['benefits'].keys())[3:]:
            self.assertTrue(results['data']['benefits'][key] != 0)
        dob = self.today - datetime.timedelta(days=365*63)
        results = interpolate_benefits(mock_results, 2176, (66, 0), 63, dob)
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

    def test_parse_response(self):
        result = parse_response({}, '', 'en')
        self.assertTrue(result[1] == 0)
        self.assertTrue('error' in result[0])
        self.assertTrue('responding' in result[0]['note'])
        result = parse_response({}, '', 'es')
        self.assertTrue('error' in result[0])
        self.assertTrue('respondiendo' in result[0]['note'])
        self.assertTrue(result[1] == 0)

    def test_interpolate_for_past_fra(self):
        mock_results = {'data': {'early retirement age': '',
                                 'full retirement age': '',
                                 'benefits': {'age 62': 0,
                                              'age 63': 0,
                                              'age 64': 0,
                                              'age 65': 0,
                                              'age 66': 0,
                                              'age 67': 0,
                                              'age 68': 0,
                                              'age 69': 1431,
                                              'age 70': 1545,
                                              },
                                 'params': self.sample_params,
                                 'disability': '',
                                 'months_past_birthday': 0,
                                 'survivor benefits': {
                                        'child': '',
                                        'spouse caring for child': '',
                                        'spouse at full retirement age': '',
                                        'family maximum': ''
                                        }
                                 },
                        'current_age': 68,
                        'error': '',
                        'note': '',
                        'past_fra': True,
                        }
        eleven_month_edge = self.today.replace(day=1).replace(year=self.today.year-69).replace(month=self.today.month + 1)
        results = interpolate_for_past_fra(mock_results, 1431, 68, eleven_month_edge)
        self.assertTrue(results['data']['benefits']['age 70'] == 1545)

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
        one_one = "{0}".format(date(1980, 1, 1).replace(year=self.today.year-25))
        way_old = "{0}".format(self.today-timedelta(days=80*365))
        too_old = "{0}".format(self.today-timedelta(days=68*365))
        ok = "{0}".format(self.today-timedelta(days=57*365))
        too_young = "{0}".format(self.today-timedelta(days=21*365))
        future = "{0}".format(self.today+timedelta(days=365))
        edge = "{0}".format(self.today-timedelta(days=67*365))
        invalid = "xx/xx/xxxx"
        self.assertTrue(past_fra_test(one_one, language='en') == False)
        self.assertTrue(past_fra_test(too_old, language='en') == True)
        self.assertTrue(past_fra_test(too_old, language='es') == True)
        self.assertTrue(past_fra_test(ok, language='en') == False)
        self.assertTrue("22" in past_fra_test(too_young, language='en'))
        self.assertTrue("sentimos" in past_fra_test(too_young, language='es'))
        self.assertTrue("22" in past_fra_test(future, language='en'))
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
        params = copy(self.sample_params)
        data_keys = [u'early retirement age',
                     u'full retirement age',
                     u'benefits',
                     u'params',
                     u'disability',
                     u'months_past_birthday',
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
        data = get_retire_data(params, language='en')['data']
        self.assertEqual(data['params']['yob'], 1970)
        for each in data.keys():
            self.assertTrue(each in data_keys)
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)
        params['dobday'] = 1
        params['dobmon'] = 6
        data = get_retire_data(params, language='en')['data']
        self.assertEqual(data['params']['yob'], 1970)
        params['yob'] = self.today.year-62
        params['dobmon'] = self.today.month
        params['dobday'] = self.today.day
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 62'] != 0)
        params['yob'] = 1937
        data = get_retire_data(params, language='en')
        self.assertEqual(data['data']['params']['yob'], 1937)
        self.assertTrue('70' in data['note'])
        params['yob'] = self.today.year-21
        data = get_retire_data(params, language='en')
        self.assertTrue("22" in data['note'])
        params['yob'] = self.today.year-57
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 62'] != 0)
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-64
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-65
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-66
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.assertTrue(data['data']['benefits']['age 66'] != 0)
        params['yob'] = self.today.year-67
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-68
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-69
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['yob'] = self.today.year-70
        data = get_retire_data(params, language='en')
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        params['earnings'] = 0
        data = get_retire_data(params, language='en')
        self.assertTrue("zero" in data['error'])
        params['yob'] = self.today.year-45
        data = get_retire_data(params, language='en')
        self.assertTrue("zero" in data['error'] or "SSA" in data['error'])
        params['earnings'] = 100000
        params['yob'] = self.today.year-68
        data = get_retire_data(params, language='en')
        self.assertTrue("past" in data['note'])
        params['yob'] = self.today.year + 1
        data = get_retire_data(params, language='en')
        self.assertTrue("22" in data['note'])

    @mock.patch('retirement_api.utils.ss_calculator.requests.post')
    def test_bad_calculator_requests(self, mock_requests):
        params = copy(self.sample_params)
        mock_requests.return_value.ok = False
        mock_results = get_retire_data(params, language='en')
        self.assertTrue('not responding' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.RequestException
        mock_results = get_retire_data(params, language='en')
        self.assertTrue('request error' in mock_results['error'])
        mock_results = get_retire_data(params, language='es')
        self.assertTrue('request error' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.ConnectionError
        mock_results = get_retire_data(params, language='en')
        self.assertTrue('connection error' in mock_results['error'])
        mock_requests.side_effect = requests.exceptions.Timeout
        mock_results = get_retire_data(params, language='en')
        self.assertTrue('timed out' in mock_results['error'])
        mock_requests.side_effect = ValueError
        mock_results = get_retire_data(params, language='en')
        self.assertTrue('SSA' in mock_results['error'])
