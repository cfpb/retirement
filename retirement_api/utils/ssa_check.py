# utilities for checking results from SSA's Quick Calculator
import sys
import datetime
from copy import copy
import json

from django.http import HttpRequest
from .ss_calculator import get_retire_data
from ..models import Calibration

SSA_PARAMS = {
    'dobmon': 0,
    'dobday': 0,
    'yob': 0,
    'earnings': 40000,
    'lastYearEarn': '',
    'lastEarn': '',
    'retiremonth': '',
    'retireyear': '',
    'dollars': 1,
    'prgf': 2
}


def get_test_params(age, dob_day, dob_year=None, income=40000):
    params = copy(SSA_PARAMS)
    today = datetime.date.today()
    dob = today.replace(year=(today.year - age), day=dob_day)
    if dob_year:
        dob = dob.replace(year=dob_year)
    if dob_day > today.day:
        if today.month == 1:
            dob = dob.replace(year=(dob.year - 1), month=12)
        else:
            dob = dob.replace(month=(dob.month - 1))
    params['dobmon'] = dob.month
    params['dobday'] = dob.day
    params['yob'] = dob.year
    params['earnings'] = income
    return params


TESTS = {
    'born-on-1st-age-46': get_test_params(46, 1),
    'born-on-2nd-age-46': get_test_params(46, 2),
    'born-on-3rd-age-46': get_test_params(46, 3),
    'born_on_3rd_in_1946': get_test_params(46, 3, dob_year=1946),
    'born_on_3rd_in_1947': get_test_params(46, 3, dob_year=1947),
    'born_on_3rd_in_1948': get_test_params(46, 3, dob_year=1948),
    'born_on_3rd_in_1949': get_test_params(46, 3, dob_year=1949),
    'born_on_3rd_in_1950': get_test_params(46, 3, dob_year=1950),
    'born_on_3rd_in_1951': get_test_params(46, 3, dob_year=1951),
    'born_on_3rd_in_1952': get_test_params(46, 3, dob_year=1952),
    'born_on_3rd_in_1953': get_test_params(46, 3, dob_year=1953),
    'born_on_3rd_in_1954': get_test_params(46, 3, dob_year=1954),
    'born_on_3rd_in_1955': get_test_params(46, 3, dob_year=1955),
    'born_on_3rd_in_1956': get_test_params(46, 3, dob_year=1956),
    'born_on_3rd_in_1957': get_test_params(46, 3, dob_year=1957),
    'born_on_3rd_in_1958': get_test_params(46, 3, dob_year=1958),
    'born_on_3rd_in_1959': get_test_params(46, 3, dob_year=1959),
    'born_on_3rd_in_1960': get_test_params(46, 3, dob_year=1960),
    'born_on_3rd_in_1970': get_test_params(46, 3, dob_year=1970),
}


def check_results(test_data):
    """Ensure test results match expectations saved in latest Calibration"""
    today = datetime.date.today()
    error_msg = "Mismatches found on {0}".format(today)
    OK = True
    calibration = Calibration.objects.order_by('-created').first()
    target_result_set = json.loads(calibration.results_json)
    for slug in test_data:
        target_results = target_result_set[slug]
        test_results = test_data[slug]
        for key in ['note',
                    'params_adjusted',
                    'current_age',
                    'past_fra',
                    'error']:
            if test_results[key] != target_results[key]:
                OK = False
                error_msg += "\n{0}: base param {1} did not match {2}".format(
                                slug,
                                key,
                                target_results[key])
        for data_key in ['months_past_birthday', 'full retirement age']:
            if test_results['data'][data_key] != target_results['data'][data_key]:
                OK = False
                error_msg += "\n{0}: data param {1} did not match {2}".format(
                                slug,
                                data_key,
                                target_results['data'][data_key])
        for benefit_key in target_results['data']['benefits'].keys():
            if test_results['data']['benefits'][benefit_key] != target_results['data']['benefits'][benefit_key]:
                OK = False
                error_msg += "\n{0}: benefit param {1} did not match {2}".format(
                               slug,
                               benefit_key,
                               target_results['data']['benefits'][benefit_key])
        for ssa_param_key in target_results['data']['params'].keys():
            if test_results['data']['params'][ssa_param_key] != target_results['data']['params'][ssa_param_key]:
                OK = False
                error_msg += "\n{0}: ssa param {1} did not match {2}".format(
                                slug,
                                ssa_param_key,
                                target_results['data']['params'][ssa_param_key])
    if OK:
        return "All tests pass on {0}".format(today)
    else:
        print error_msg
        return error_msg


def run_tests(recalibrate=False):
    collector = {}
    tstamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
    for test in TESTS:
        sys.stdout.write('.')
        sys.stdout.flush()
        collector[test] = get_retire_data(TESTS[test], language='en')
    if recalibrate:
        new_calibration = Calibration(results_json=json.dumps(collector))
        new_calibration.save()
        # with open("/tmp/calibration_{0}.json".format(tstamp), 'w') as f:
        #     f.write(json.dumps(collector, indent=4, sort_keys=True))
        return "New Calibration set saved: {0}".format(new_calibration)
    else:
        return check_results(collector)
