# script to check the retirement api to make sure
# the SSA Quick Calculator is operational
# and to log the result to a csv (currently via cron)
import requests
import datetime
import json
import time
import signal

timestamp = datetime.datetime.now()

# rolling dob to guarantee subject is 44 and full retirement age is 67
dob = timestamp - datetime.timedelta(days=44*365+30)
timeout_seconds = 15


class TimeoutError(Exception):
    pass


def handler(signum, frame):
    raise TimeoutError("Request timed out")


class Collector(object):
    data = ''
    date = "%s" % timestamp
    status = ''
    error = ''
    note = ''
    api_fail = ''
    timer = ''

collector = Collector()
log_header = ['data', 'date', 'status', 'error', 'note', 'api_fail', 'timer']

local_base = 'http://localhost:8080'
api_base = 'retirement/retirement-api'
api_string = '%s/%s/estimator/%s-%s-%s/70000/'


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


def run(base):
    url = api_string % (base, api_base, dob.month, dob.day, dob.year)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    start = time.time()
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
        collector.error = 'SSA request exceeded 15 sec'
        collector.api_fail = 'FAIL'
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
    collector.timer = "%s" % (end - start)
    print_msg(collector)
    print url
    return collector

if __name__ == '__main__':
    """runs against a local url unless a domain is passed
    """

    try:
        base = sys.argv[1]
    except:
        base = local_base
    run(base)
