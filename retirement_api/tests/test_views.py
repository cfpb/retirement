import sys
import os
import datetime
import json

import mock

from django.shortcuts import render_to_response
from django.template import RequestContext

# if __name__ == '__main__':
#     BASE_DIR = '~/Projects/retirement1.6/retirement/retirement_api'
# else:
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import unittest
from django.http import HttpRequest
from retirement_api.views import param_check, income_check, estimator, get_full_retirement_age, claiming
from retirement_api.utils.ss_calculator import get_retire_data, params

today = datetime.datetime.now().date()

class ViewTests(unittest.TestCase):
    req_base = HttpRequest()
    req_good = HttpRequest()
    req_good.GET['dob'] = '1955-05-05'
    req_good.GET['income'] = '40000'
    req_blank = HttpRequest()
    req_blank.GET['dob'] = ''
    req_blank.GET['income'] = ''
    req_invalid = HttpRequest()
    req_invalid.GET['dob'] = '1-2-%s' % (today.year + 5)
    req_invalid.GET['income'] = 'x'
    return_keys = ['data', 'error']

    def test_base_view(self):
        # response = claiming(req_base)
        mock_render_to_response = mock.MagicMock()
        with mock.patch.multiple('retirement_api.views',
            render_to_response=mock_render_to_response,
            RequestContext=mock.MagicMock()):
            from retirement_api.views import claiming
            mock_request = mock.Mock()
            claiming(mock_request)
            _, args, _ = mock_render_to_response.mock_calls[0]
            self.assertEquals(args[0], 'claiming.html',
                            'The wrong template is in our render')
            self.assertEquals(args[1]['available_languages'], ['en', 'es'],
                            'Passing the wrong available_languages variable in')

    def test_param_check(self):
        self.assertEqual(param_check(self.req_good, 'dob'), '1955-05-05')        
        self.assertEqual(param_check(self.req_good, 'income'), '40000')
        self.assertEqual(param_check(self.req_blank, 'dob'), None)        
        self.assertEqual(param_check(self.req_blank, 'income'), None)        

    def test_income_check(self):
        self.assertEqual(income_check('544.30'), 544)
        self.assertEqual(income_check('$55,000.15'), 55000)
        self.assertEqual(income_check('0'), 0)
        self.assertEqual(income_check('x'), None)
        self.assertEqual(income_check(''), None)

    def test_get_full_retirement_age(self):
        request = self.req_blank
        response = get_full_retirement_age(request, birth_year='1953')
        self.assertTrue(json.loads(response.content) == [66, 0])
        response2 = get_full_retirement_age(request, birth_year=1957)
        self.assertTrue(json.loads(response2.content) == [66, 6])
        response3 = get_full_retirement_age(request, birth_year=1969)
        self.assertTrue(json.loads(response3.content) == [67, 0])
        response4 = get_full_retirement_age(request, birth_year=969)
        self.assertTrue(response4.status_code == 400)

    def test_estimator_url_data(self):
        request = self.req_blank
        response = estimator(request, dob='1955-05-05', income='40000')
        self.assertTrue(type(response.content) == str)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_url_data_bad_income(self):
        request = self.req_blank
        response = estimator(request, dob='1955-05-05', income='z')
        self.assertTrue(response.status_code == 400)

    def test_estimator_url_data_bad_dob(self):
        request = self.req_blank
        response = estimator(request, dob='1955-05-xx', income='4000')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data(self):
        request = self.req_good
        response = estimator(request)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(type(response.content) == str)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_query_data_blank(self):
        request = self.req_blank
        response = estimator(request)
        self.assertTrue(response.status_code == 400)
    
    def test_estimator_query_data_blank_dob(self):
        request = self.req_blank
        response = estimator(request, income='40000')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_blank_income(self):
        request = self.req_blank
        response = estimator(request, dob='1955-05-05')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_bad_dob(self):
        request = self.req_invalid
        response = estimator(request, income='40000')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_bad_dob_of_today(self):
        request = self.req_blank
        response = estimator(request, income='40000', dob="%s" % today)
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_bad_income(self):
        request = self.req_invalid
        response = estimator(request, dob='1955-05-05')
        self.assertTrue(response.status_code == 400)
