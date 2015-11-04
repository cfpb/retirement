# script to check the retirement api to make sure
# the SSA Quick Calculator is operational
# and to log the result to a csv (currently via cron)
import os
import sys
import requests
import datetime
import json
import time
import random
import signal
from urlparse import urlparse

timestamp = datetime.datetime.now()
default_base = 'build'

# rolling dob to guarantee subject is 44 and full retirement age is 67
dob = timestamp - datetime.timedelta(days=44*365+60)
timeout_seconds = 20

API_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError("Request timed out")


class Collector(object):
    data = ''
    date = ("%s" % timestamp)[:16]
    domain = ''
    status = ''
    error = ''
    note = ''
    api_fail = ''
    timer = ''

collector = Collector()
log_header = ['data',
              'date',
              'domain',
              'status',
              'error',
              'api_fail',
              'timer']


def print_msg(collector):
    msg = ",".join([collector.__getattribute__(key) for key in log_header])
    print msg
    return msg


def check_data(data):
    """ For a 44-year-old, the api should
        always return an age, a full retirement age
        and a value for benefits at age 70
    """
    if (data['current_age'] == 44 and
            data['data']['full retirement age'] == '67' and
            data['data']['benefits']['age 70']):
        return "OK"
    else:
        return "BAD DATA"

prefix = 'http://'
suffix = '.consumerfinance.gov/retirement'
api_string = 'retirement-api/estimator/%s-%s-%s/%s/' % (dob.month,
                                                           random.randrange(1, 28),
                                                           dob.year,
                                                           random.randrange(20000, 100000))
BASES = {
    'unitybox': 'http://localhost:8080/retirement',
    'standalone': 'http://localhost:8000',
    default_base: '%s%s%s' % (prefix, default_base, suffix),
    'prod': '%swww%s' % (prefix, suffix),
    }


def run(base):
    url = "%s/%s" % (base, api_string)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    start = time.time()
    print "trying request at %s" % url
    try:
        test_request = requests.get(url)
    except requests.ConnectionError:
        end = time.time()
        signal.alarm(0)
        collector.status = "ABORTED"
        collector.error = 'Server connection error'
        collector.api_fail = 'FAIL'
    except TimeoutError:
        end = time.time()
        signal.alarm(0)
        collector.status = "TIMEDOUT"
        collector.error = 'SSA request exceeded %s sec' % timeout_seconds
    else:
        if test_request.status_code != 200:
            signal.alarm(0)
            end = time.time()
            collector.status = "%s" % test_request.status_code
            collector.error = test_request.reason
            collector.api_fail = 'FAIL'
        else:
            end = time.time()
            signal.alarm(0)
            data = json.loads(test_request.text)
            collector.status = "%s" % test_request.status_code
            collector.error = data['error']
            collector.note = data['note']
            collector.data = check_data(data)
            if collector.data == "BAD DATA":
                collector.api_fail = 'FAIL'
    collector.timer = "%s" % round(end - start, 1)
    msg = print_msg(collector)
    with open('%s/tests/logs/api_check.log' % API_ROOT, 'a') as f:
        f.write("%s\n" % msg)
    return collector

if __name__ == '__main__':
    """
    runs against one of these base urls:
    unitybox, standalone, build, or prod;
    defaults to build
    """
    helpmsg = "pass a base to test: unitybox, standalone, build, or prod"
    try:
        BASE = sys.argv[1]
    except:
        collector.domain = default_base
        run(BASES[default_base])
    else:
        if BASE in BASES:
            collector.domain = BASE
            run(BASES[BASE])
        else:
            print helpmsg
            sys.exit()
