import os
import sys
import json
import datetime

import mock
import unittest

from ..check_api import Collector, print_msg, check_data, run
timestamp = datetime.datetime.now()


class TestApi(unittest.TestCase):
    """test the tester"""
    test_collector = Collector()
    test_data = {
        'current_age': 44,
        'note': "",
        'data': {
            'benefits': {
                'age 63': 1603,
                'age 62': 1476,
                'age 67': 2137,
                'age 66': 1995,
                'age 65': 1852,
                'age 64': 1710,
                'age 69': 2479,
                'age 68': 2308,
                'age 70': 2650
                },
            'disability': "$1,899",
            'early retirement age': "62 and 1 month",
            'params': {
                'dollars': 1,
                'lastYearEarn': "",
                'dobday': 7,
                'prgf': 2,
                'dobmon': 7,
                'retiremonth': "",
                'retireyear': "",
                'yob': 1970,
                'lastEarn': "",
                'earnings': 70000
                },
            'full retirement age': "67",
            'survivor benefits': {
                'spouse at full retirement age': "$1,912",
                'family maximum': "$3,377",
                'spouse caring for child': "$1,434",
                'child': "$1,434"
                }
            },
        'error': ""
        }

    def test_check_data(self):
        msg = check_data(self.test_data)
        self.assertTrue(msg == 'OK')

    def test_print_msg(self):
        target_text = ',%s,,,,,' % self.test_collector.date
        test_text = print_msg(self.test_collector)
        print "test_text: %s" % test_text
        print "target_text: %s" % target_text
        self.assertTrue(test_text == target_text)

    @mock.patch('retirement.retirement_api.utils.check_api.requests')
    @mock.patch('retirement.retirement_api.utils.check_api.print_msg')
    def test_run(self, mock_print_msg, mock_requests):
        mock_requests.return_value.text = json.dumps(self.test_data)
        mock_requests.return_value.status_code = 200
        run('fake.com')
        self.assertTrue(mock_print_msg.call_count == 1)
