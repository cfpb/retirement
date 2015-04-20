import datetime
import json

import mock

import unittest
from django.http import HttpRequest
from .views import param_check, income_check, estimator, get_full_retirement_age
from .utils.ss_calculator import get_retire_data, params

today = datetime.datetime.now().date()

class ViewTests(unittest.TestCase):
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
