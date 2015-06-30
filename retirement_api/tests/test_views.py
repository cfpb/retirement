import sys
import os
import datetime
import json

import mock
import unittest

from django.http import HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import retirement_api.views
today = datetime.datetime.now().date()


class ViewTests(unittest.TestCase):
    fixtures = ['retiredata.json']
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
        mock_render_to_response = mock.MagicMock()
        with mock.patch.multiple('retirement_api.views',
                                 render_to_response=mock_render_to_response,
                                 RequestContext=mock.MagicMock()):
            # from retirement_api.views import claiming
            mock_request = mock.Mock()
            retirement_api.views.claiming(mock_request)
            _, args, _ = mock_render_to_response.mock_calls[0]
            self.assertEquals(args[0], 'claiming.html',
                              'The wrong template is in our render')
            self.assertEquals(args[1]['available_languages'], ['en', 'es'],
                              'Passing the wrong available_languages variable')
            retirement_api.views.claiming(mock_request, es=True)
            _, args, _ = mock_render_to_response.mock_calls[0]
            self.assertEquals(args[1]['available_languages'], ['en', 'es'],
                              'Passing the wrong available_languages variable')

    def test_param_check(self):
        self.assertEqual(retirement_api.views.param_check(self.req_good, 'dob'), '1955-05-05')
        self.assertEqual(retirement_api.views.param_check(self.req_good, 'income'), '40000')
        self.assertEqual(retirement_api.views.param_check(self.req_blank, 'dob'), None)
        self.assertEqual(retirement_api.views.param_check(self.req_blank, 'income'), None)

    def test_income_check(self):
        self.assertEqual(retirement_api.views.income_check('544.30'), 544)
        self.assertEqual(retirement_api.views.income_check('$55,000.15'), 55000)
        self.assertEqual(retirement_api.views.income_check('0'), 0)
        self.assertEqual(retirement_api.views.income_check('x'), None)
        self.assertEqual(retirement_api.views.income_check(''), None)

    def test_get_full_retirement_age(self):
        request = self.req_blank
        response = retirement_api.views.get_full_retirement_age(request, birth_year='1953')
        self.assertTrue(json.loads(response.content) == [66, 0])
        response2 = retirement_api.views.get_full_retirement_age(request, birth_year=1957)
        self.assertTrue(json.loads(response2.content) == [66, 6])
        response3 = retirement_api.views.get_full_retirement_age(request, birth_year=1969)
        self.assertTrue(json.loads(response3.content) == [67, 0])
        response4 = retirement_api.views.get_full_retirement_age(request, birth_year=969)
        self.assertTrue(response4.status_code == 400)

    def test_estimator_url_data(self):
        request = self.req_blank
        response = retirement_api.views.estimator(request, dob='1955-05-05', income='40000')
        self.assertTrue(type(response.content) == str)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_url_data_bad_income(self):
        request = self.req_blank
        response = retirement_api.views.estimator(request, dob='1955-05-05', income='z')
        self.assertTrue(response.status_code == 400)

    def test_estimator_url_data_bad_dob(self):
        request = self.req_blank
        response = retirement_api.views.estimator(request, dob='1955-05-xx', income='4000')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data(self):
        request = self.req_good
        response = retirement_api.views.estimator(request)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(type(response.content) == str)
        rdata = json.loads(response.content)
        for each in self.return_keys:
            self.assertTrue(each in rdata.keys())

    def test_estimator_query_data_blank(self):
        from retirement_api.views import estimator
        request = self.req_blank
        response = retirement_api.views.estimator(request)
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_blank_dob(self):
        request = self.req_blank
        response = retirement_api.views.estimator(request, income='40000')
        self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_blank_income(self):
        request = self.req_blank
        response = retirement_api.views.estimator(request, dob='1955-05-05')
        self.assertTrue(response.status_code == 400)

    # def test_estimator_query_data_bad_dob(self):
    #     request = self.req_invalid
    #     response = estimator(request, income='40000')
    #     self.assertTrue(response.status_code == 400)

    # def test_estimator_query_data_bad_dob_of_today(self):
    #     request = self.req_blank
    #     response = estimator(request, income='40000', dob="%s" % today)
    #     self.assertTrue(response.status_code == 400)

    def test_estimator_query_data_bad_income(self):
        request = self.req_invalid
        response = retirement_api.views.estimator(request, dob='1955-05-05')
        self.assertTrue(response.status_code == 400)
