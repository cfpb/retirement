import os
import sys
import json
import datetime
from datetime import timedelta

import mock
import unittest

from ..ss_utilities import get_retirement_age, get_delay_bonus, yob_test
from ..ss_utilities import age_map, past_fra_test, get_current_age
from ..ss_calculator import num_test, parse_details, requests
from ..ss_calculator import interpolate_benefits, get_retire_data

today = datetime.datetime.now().date()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

# from ...utils import ss_update_stats
# from retirement_api import utils


class UtilitiesTests(unittest.TestCase):
    fixtures = ['retiredata.json']
    sample_params = {
        'dobmon': 1,
        'dobday': 1,
        'yob': 1970,
        'earnings': 70000,
        'lastYearEarn': '',
        'lastEarn': '',
        'retiremonth': '',
        'retireyear': '',
        'dollars': 1,
        'prgf': 2
    }

    @mock.patch('datetime.date')
    def test_get_current_age(self, mock_datetime):
        fake_today = datetime.datetime(2000, 1, 2).date()
        mock_datetime.today.return_value = fake_today
        age_pairs = [('1999-1-1', 1),
                     ('1980-1-1', 20),
                     ('1980-1-3', 19),
                     ('1940-1-1', 60),
                     ('1920-1-1', 80),
                     ('2001-1-1', None),
                     ('1999-1-xx', None),
                     ('2000-1-2', None),
                     ('1999-1-3', 0)]
        print "fake_today is %s" % fake_today
        for pair in age_pairs:
            print "get_current_age(%s) is %s" % (pair[0],
                                                 get_current_age(pair[0]))
            self.assertEqual(get_current_age(pair[0]), pair[1])
        fake_today = datetime.datetime(2005, 2, 28).date()
        mock_datetime.today.return_value = fake_today
        self.assertEqual(get_current_age('2000-2-29'), 5)

    def test_interpolate_benefits(self):
        benefits = {
            'age 62': 1602,
            'age 63': 0,
            'age 64': 0,
            'age 65': 0,
            'age 66': 0,
            'age 67': 2261,
            'age 68': 0,
            'age 69': 0,
            'age 70': 0,
            }
        results = {
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
        bens = interpolate_benefits(benefits, (67, 0), 44)
        for key in bens.keys():
            self.assertEqual(bens[key], results[key])
        benefits['age 66'] = benefits['age 67']
        benefits['age 67'] = 0
        bens = interpolate_benefits(benefits, (66, 0), 55)
        for key in sorted(bens.keys()):
            self.assertTrue(bens[key] != 0)
        bens = interpolate_benefits(benefits, (66, 0), 64)
        for key in sorted(bens.keys())[2:]:
            self.assertTrue(bens[key] != 0)
        bens = interpolate_benefits(benefits, (66, 0), 65)
        for key in sorted(bens.keys())[3:]:
            self.assertTrue(bens[key] != 0)

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
        self.assertTrue("least 22" in past_fra_test(too_young))
        self.assertTrue("invalid birth" in past_fra_test(invalid))
        print "'way_old' fra_test returns %s" % past_fra_test(way_old)
        self.assertTrue("older" in past_fra_test(way_old))
        self.assertTrue(past_fra_test(edge) == True)

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
        data = json.loads(get_retire_data(self.sample_params))['data']
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['params']['yob'], 1970)
        for each in data.keys():
            self.assertTrue(each in data_keys)
        for each in data['benefits'].keys():
            self.assertTrue(each in benefit_keys)
        self.sample_params['yob'] = 1937
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data['data']['params']['yob'], 1937)
        self.assertTrue('older' in data['note'])
        self.sample_params['yob'] = 193
        data = json.loads(get_retire_data(self.sample_params))
        print "'invalid' error is returning %s" % data['error']
        self.assertTrue("too old" in data['error'])
        self.sample_params['yob'] = today.year-21
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue("least 22" in data['note'])
        self.sample_params['yob'] = today.year-57
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 62'] != 0)
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-64
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-65
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-66
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.assertTrue(data['data']['benefits']['age 66'] != 0)
        self.sample_params['yob'] = today.year-67
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-68
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-69
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)
        self.sample_params['yob'] = today.year-70
        data = json.loads(get_retire_data(self.sample_params))
        self.assertTrue(data['data']['benefits']['age 70'] != 0)

    # @mock.patch('utils.ss_calculator.requests')
    # def test_ss_calculator_bad_request(self, mock_request):
    #     mock_request.post.return_value.reason = 'Not found'
    #     # self.sample_params['lastYearEarn'] = 19
    #     result_json = utils.ss_calculator.get_retire_data(self.sample_params)
    #     results = json.loads(result_json)
    #     print "results error message is %s" % results['error']
    #     self.assertTrue('failed' in results['error'])


        