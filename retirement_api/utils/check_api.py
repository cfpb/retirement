# script to check the retirement api to make sure
# the SSA Quick Calculator is operational
# and to log the result to a csv (currently via cron)
import requests
import datetime
import json

timestamp = datetime.datetime.now()

# rolling dob to guarantee subject is 44 and full retirement age is 67
dob = timestamp - datetime.timedelta(days=44*365+30)


class Collector(object):
    data = ''
    date = "%s" % timestamp
    status = ''
    error = ''
    note = ''
    api_fail = 'False'

collector = Collector()
log_header = ['data', 'date', 'status', 'error', 'note', 'api_fail']

local_base = 'http://localhost:8080'
build_base = 'http://build.consumerfinance.gov'
live_base = 'http://www.consumerfinance.gov'
api_base = '/retirement/retirement-api'
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
    test_request = requests.get(url)
    if test_request.status_code != 200:
        collector.status = "%s" % test_request.status_code
        collector.error = test_request.reason
        collector.api_fail = 'True'
        print_msg(collector)
        return collector
    else:
        data = json.loads(test_request.text)
        collector.status = "%s" % test_request.status_code
        collector.error = data['error']
        collector.note = data['note']
        collector.data = check_data(data)
        print_msg(collector)
        return collector

if __name__ == '__main__':
    """runs against a local url unless a domain is passed
    """

    try:
        base = sys.argv[1]
    except:
        base = local_base
    run(base)
