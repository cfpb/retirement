"""
users must be at least 22 to use the form
users past their full retirement age will get only their current benefit amount

Well need to ask user for DOB and current annual earnings
returns estimated benefit at 62, 67, and 70 based the value of the dollar today

inputs needed:
    Date of birth: 8/14/1956
    Current earnings: 50000

optional inputs (not currently used):
    Last year with earnings
    Last earnings
    Retirement month/year: 8/2026
    Benefit in inflated dollars; we're using default of current-year dollars
"""
import re
import requests
import json
import datetime
import math
import lxml
import time
import signal

from bs4 import BeautifulSoup as bs
from .ss_utilities import get_retirement_age, get_current_age, past_fra_test
from .check_api import TimeoutError, handler

timeout_seconds = 10

down_note = "\
The Social Security website is not responding, \
so we can't estimate your benefits right now. \
Please try again in a few minutes.\
"

base_url = "http://www.ssa.gov"
quick_url = "%s/OACT/quickcalc/" % base_url  # where users go; not needed here
result_url = "%s/cgi-bin/benefit6.cgi" % base_url
chart_ages = range(62, 71)

comment = re.compile(r"<!--[\s\S]*?-->")  # regex for parsing indexing data


def clean_comment(comment):
    return comment.replace('<!--', '').replace('-->', '').strip()

# unused; would need a test
# def parse_comments(req, results):
#     """
#     this pulls indexing details out of the source comments
#     on SSA's quick-calculator results page
#     and adds it to the results payload;
#     we are not yet using this data
#     """
#     raw_comments = comment.findall(req.text)
    # comments = [clean_comment(com) for com in raw_comments if
    #             clean_comment(com) and not
    #             clean_comment(com).startswith('Indexed') and not
    #             clean_comment(com).startswith('Nominal')]
#     headings = [term.strip() for term in comments[0].split()]
#     headings.pop(headings.index('max'))
#     headings[headings.index('Tax')] = 'Tax_max'
#     detail_rows = []
#     details = []
#     for row in comments[1:]:
#         if num_test(row.split()[0]):
#             detail_rows.append([cell.strip() for cell in row.split()])
#         else:
#             details.append(row)
    # for row in detail_rows:
    #     results['earnings_data'].append({tup[0]: tup[1] for tup
    #                                      in zip(headings, row)})
#     results['benefit_details']['family_max'] = details.pop(-1)
#     results['benefit_details']['indexing']={}
#     INDEXING = results['benefit_details']['indexing']
#     sets = len(details) / 3
#     i1, i2 = (-3, 0)
#     for i in range(sets):
#         i1 += 3
#         i2 += 3
#         INDEXING.update(parse_details(details[i1:i2]))
#     return results


def num_test(value=''):
    try:
        num = int(value)
    except:
        try:
            num = int(float(value))
        except:
            return False
        else:
            return True
    else:
        return True


# unused for now
def parse_details(rows):
    datad = {}
    if len(rows) == 3:
        titlerow = rows[0].split(':')
        datad[titlerow[0].strip().upper()] = {'Bend points':
                                              titlerow[1].strip()}
        outer = datad[titlerow[0].strip().upper()]
        outer['AIME'] = rows[1]
        outer['COLA'] = rows[2]
    return datad


def interpolate_benefits(benefits, fra_tuple, current_age):
    """
    estimates missing benefit values, because SSA provides no more than 3
    need to handle these cases:
        FRA could be 66, or 67 (folks with FRA of 65 older than their FRA)
        visitor could be between the ages of 55 and 65
            their FRA is 66, which changes where we need to fill in the chart
        visitor could be too young to use the tool (< 22)
        visitor's age could be past FRA; only current benefit is returned
            if current age is 67, 68, 69 or 70+
    """
    fra = fra_tuple[0]  # could be 66 or 67
    # if not fra:
    #     return benefits
    # fill out the missing years, working backward and forward from the FRA
    if fra == 67:
        base = benefits['age 67']
        benefits['age 62'] = int(round(base - base*(3*12*(0.00555555)) -
                                       base*(2*11*0.004166666)))
        benefits['age 63'] = int(round(base - base*(3*12*(0.00555555)) -
                                       base*(1*12*0.004166666)))
        benefits['age 64'] = int(round(base - base*(3*12*(0.00555555))))
        benefits['age 65'] = int(round(base - base*(2*12*(0.00555555))))
        benefits['age 66'] = int(round(base - base*(1*12*(0.00555555))))
        benefits['age 68'] = int(round(base + (base * 0.08)))
        benefits['age 69'] = int(round(base + (2 * (base * 0.08))))
        benefits['age 70'] = int(round(base + (3 * (base * 0.08))))
    elif fra == 66 and current_age < 66:
        base = benefits['age 66']
        month_increment = (base * 0.08)/12
        diff_forward = 12 - fra_tuple[1]
        diff_back = 12 + fra_tuple[1]
        benefits['age 67'] = int(round(base +
                                 (month_increment*diff_forward)))
        benefits['age 68'] = int(round(base +
                                 (month_increment*(12 + diff_forward))))
        benefits['age 69'] = int(round(base +
                                 (month_increment*(24 + diff_forward))))
        benefits['age 70'] = int(round(base +
                                 (month_increment*(36 + diff_forward))))
        if current_age == 65:
            # FRA is 66; need to fill in 65
            benefits['age 62'] = 0
            benefits['age 63'] = 0
            benefits['age 64'] = 0
            benefits['age 65'] = int(round(base -
                                     base*(diff_back*(0.00555555))))
        elif current_age == 64:
            # FRA is 66; need to fill in 64 and 65
            benefits['age 62'] = 0
            benefits['age 63'] = 0
            benefits['age 64'] = int(round(base -
                                     base*((diff_back + 12)*(0.00555555))))
            benefits['age 65'] = int(round(base -
                                     base*(diff_back*(0.00555555))))
        elif current_age in range(55, 64):
            # ages 55 to 63: FRA is 66; need to fill in 62, 63, 64 and 65
            benefits['age 62'] = int(round(base -
                                     base*((diff_back + 24)*(0.00555555)) -
                                     base*(1*11*0.004166666)))
            benefits['age 63'] = int(round(base -
                                     base*((diff_back + 24)*(0.00555555))))
            benefits['age 64'] = int(round(base -
                                     base*((diff_back + 12)*(0.00555555))))
            benefits['age 65'] = int(round(base -
                                     base*(diff_back*(0.00555555))))
    return benefits

# sample params
params = {
    'dobmon': 8,
    'dobday': 14,
    'yob': 1970,
    'earnings': 70000,
    'lastYearEarn': '',  # possible use for unemployed or already retired
    'lastEarn': '',  # possible use for unemployed or already retired
    'retiremonth': '',  # leve blank to get triple calculation -- 62, 67 and 70
    'retireyear': '',  # leve blank to get triple calculation -- 62, 67 and 70
    'dollars': 1,  # benefits to be calculated in current-year dollars
    'prgf': 2
}


def get_retire_data(params):
    starter = datetime.datetime.now()
    collector = {}
    benefits = {}
    for age in chart_ages:
        benefits["age %s" % age] = 0
    dobstring = "%s-%s-%s" % (params['yob'],
                              params['dobmon'],
                              params['dobday'])
    results = {'data': {
                    'early retirement age': '',
                    'full retirement age': '',
                    'benefits': benefits,
                    'params': params,
                    'disability': '',
                    'survivor benefits': {
                                    'child': '',
                                    'spouse caring for child': '',
                                    'spouse at full retirement age': '',
                                    'family maximum': ''
                                    }
                    },
               'current_age': 0,
               'error': '',
               'note': ''
               }
    BENS = results['data']['benefits']
    current_age = get_current_age(dobstring)
    results['current_age'] = current_age
    past_fra = past_fra_test(dobstring)
    if past_fra is False:
        pass
    elif past_fra is True:
        results['note'] = "You are past Social Security's full retirement age."
    else:  # if neither False nor True, there's an error and we need to bail
        if current_age > 70:
            results['note'] = past_fra
            results['error'] = "visitor too old for tool"
            return json.dumps(results)
        elif current_age < 22:
            results['note'] = past_fra
            results['error'] = "visitor too young for tool"
            return json.dumps(results)
        elif 'invalid' in past_fra:
            results['note'] = "An invalid date was entered."
            results['error'] = past_fra
            return json.dumps(results)
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout_seconds)
    try:
        req = requests.post(result_url, data=params)
    except requests.ConnectionError:
        signal.alarm(0)
        results['error'] = "Social Security's website is not responding.\
                            Status code: %s (%s)" % (req.status_code,
                                                     req.reason)
        results['note'] = down_note
        return json.dumps(results)
    except TimeoutError:
        signal.alarm(0)
        results['error'] = "Social Security's website is not responding."
        results['note'] = down_note
        return json.dumps(results)
    else:
        signal.alarm(0)
    if not req.ok:
        results['error'] = "Social Security's website is not responding.\
                            Status code: %s (%s)" % (req.status_code,
                                                     req.reason)
        results['note'] = down_note
        return json.dumps(results)
    if int(params['dobmon']) == 1 and int(params['dobday']) == 1:
        # SSA has a special rule for people born on Jan. 1:
        # http://www.socialsecurity.gov/OACT/ProgData/nra.html
        yob = int(params['yob']) - 1
        yobstring = "%s" % yob
    else:
        yobstring = params['yob']
    fra_tuple = get_retirement_age(yobstring)
    soup = bs(req.text, 'lxml')
    tables = soup.findAll('table', {'bordercolor': '#6699ff'})
    results_table, disability_table, survivors_table = (None, None, None)
    for each in tables:
        if each.find('th') and 'Retirement age' in each.find('th').text:
            results_table = each
        elif each.find('th') and 'Disability' in each.find('th').text:
            disability_table = each
        elif each.find('th') and "Survivors" in each.find('th').text:
            survivors_table = each
    if past_fra is True:
        results['data']['disability'] = "You have reached full retirement age \
                                and are not eligible for disability benefits."
        ret_amount = soup.find('span', {'id': 'ret_amount'}).text.split('.')[0]
        base = int(ret_amount.replace(',', ''))
        increment = base * 0.08
        if current_age == 66:
            BENS['age 66'] = round(base)
            BENS['age 67'] = round(base + increment)
            BENS['age 68'] = round(base + 2*increment)
            BENS['age 69'] = round(base + 3*increment)
            BENS['age 70'] = round(base + 4*increment)
        elif current_age == 67:
            BENS['age 67'] = round(base)
            BENS['age 68'] = round(base + increment)
            BENS['age 69'] = round(base + 2*increment)
            BENS['age 70'] = round(base + 3*increment)
        elif current_age == 68:
            BENS['age 68'] = round(base)
            BENS['age 69'] = round(base + increment)
            BENS['age 70'] = round(base + 2*increment)
        elif current_age == 69:
            BENS['age 69'] = round(base)
            BENS['age 70'] = round(base + increment)
        elif current_age == 70:
            BENS['age 70'] = round(base)
        else:  # older than 70
            BENS['age 70'] = round(base)
            results['note'] = "Your monthly benefit \
                               at %s is $%s" % (current_age, ret_amount)
    else:
        if results_table:
            result_rows = results_table.findAll('tr')
            for row in result_rows:
                cells = row.findAll('td')
                if cells:
                    collector[cells[0].text] = cells[1].text
            """
            collector:
            70 in 2047: "$2,719.00",
            67 in 2044: "$2,180.00",
            62 and 1 month in 2039: "$1,515.00"
            """
            for key in collector:
                bits = key.split(' in ')
                benefit_age_raw = bits[0]
                benefit_age_year = bits[0].split()[0]
                # benefit_in_year = bits[1]# not using
                benefit_raw = collector[key]
                benefit = int(benefit_raw.split('.')[0].replace(',', '').replace('$', ''))
                if benefit_age_year == str(fra_tuple[0]):
                    results['data']['full retirement age'] = benefit_age_raw
                    BENS['age %s' % benefit_age_year] = benefit
                # if benefit_age_year == '62':
                #     results['data']['early retirement age'] = benefit_age_raw
                #     BENS['age %s' % benefit_age_year] = benefit
                # if benefit_age_year == '70':
                #     BENS['age %s' % benefit_age_year] = benefit
            additions = interpolate_benefits(BENS, fra_tuple, current_age)
            for key in BENS:
                if additions[key] and not BENS[key]:
                    BENS[key] = additions[key]
        if disability_table:
            results['data']['disability'] = disability_table.findAll('td')[1].text.split('.')[0]
    # SURVIVORS KEYS
    # 'Your child'
    # 'Family maximum'
    # 'Your spouse at normal retirement age'
    # 'Your spouse caring for your child'
    #
    # RESULTS['DATA']['SURVIVOR BENEFITS'] KEYS
    # 'spouse at full retirement age'
    # 'family maximum'
    # 'spouse caring for child'
    # 'child'
    if survivors_table:
        SURV = results['data']['survivor benefits']
        survivors = {}
        survivor_rows = survivors_table.findAll('tr')
        for row in survivor_rows:
            cells = row.findAll('td')
            if cells:
                survivors[cells[0].text] = cells[1].text.split('.')[0]
        if 'Your child' in survivors:
            SURV['child'] = survivors['Your child']
        if 'Family maximum' in survivors:
            SURV['family maximum'] = survivors['Family maximum']
        if 'Your spouse at normal retirement age' in survivors:
            SURV['spouse at full retirement age'] = survivors['Your spouse at normal retirement age']
        if 'Your spouse caring for your child' in survivors:
            SURV['spouse caring for child'] = survivors['Your spouse caring for your child']
    if not results['data']['full retirement age']:
        if fra_tuple[1]:
            FRA = "%s and %s months" % (fra_tuple[0], fra_tuple[1])
        else:
            FRA = "%s" % fra_tuple[0]
        results['data']['full retirement age'] = FRA
    print "script took %s to run" % (datetime.datetime.now() - starter)
    # # to dump json for testing:
    # with open('/tmp/ssa.json', 'w') as f:
    #     f.write(json.dumps(results))
    return json.dumps(results)
