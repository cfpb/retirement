"""
experimenting with SS quick-calculator page as trial api for demo pages

users must be at least 22 to use the form

Well need to ask user for DOB and current annual earnings
we'll return estimated benefits at 62, 67, and 70 based the value of the dollar today

inputs needed:
    Date of birth: 8/14/1956
    Current earnings: 50000

optional inputs:
    Last year with earnings # could be useful for users who are retired or unemployed
    Last earnings # ditto
    Retirement month/year: 8/2026) # feed won't return 3 retire options if we provide this
    Benefit in year-2015 dollars) # SS can take today's dollars (1) or future, inflated dollars (0)
"""

import re
import requests
import json
import datetime
import math

from bs4 import BeautifulSoup as bs
from .ss_utilities import get_retirement_age, past_fra_test

base_url = "http://www.ssa.gov"
quick_url = "%s/OACT/quickcalc/" % base_url# where users go, but not needed for our request
result_url = "%s/cgi-bin/benefit6.cgi" % base_url

comment = re.compile(r"<!--[\s\S]*?-->")
def clean_comment(comment):
    return comment.replace('<!--', '').replace('-->', '').strip()

def num_test(value=''):
    try:
        num = int(value)
    except:
        try:
            num = int(float(value))
        except:
            return False
        else: return True
    else:
        return True

# unused for now
def parse_details(rows):
    datad = {}
    if len(rows) == 3:
        titlerow = rows[0].split(':')
        datad[titlerow[0].strip().upper()] = {'Bend points': titlerow[1].strip()}
        outer = datad[titlerow[0].strip().upper()]
        outer['AIME']  = rows[1]
        outer['COLA'] = rows[2]
    return datad

def interpolate_benefits(benefits):
    """
    estimates missing benefit values
    """
    base = None
    years = sorted(benefits.keys())
    for each in years:
        if benefits[each]:
            base = each
            break
    if not base:
        return benefits
    if base in ['age 69', 'age 70']:
        return benefits
    if base == 'age 68':
        benefits['age 69'] = (benefits['age 68'] + benefits['age 70']) / 2
        return benefits
    if base == 'age 67':
        benefits['age 68'] = round(benefits[base] + (benefits[base]* 0.08))
        benefits['age 69'] = round(benefits['age 68'] + (benefits['age 68']* 0.08))
        return benefits
    if base == 'age 66':
        if not benefits['age 67']:
            benefits['age 67'] = round(benefits['age 66'] + (benefits['age 66']* 0.08))
        benefits['age 68'] = round(benefits[base] + (benefits[base]* 0.08))
        benefits['age 69'] = round(benefits['age 68'] + (benefits['age 68']* 0.08))
        return benefits
    if benefits['age 65']:
        benefits['age 66'] = round(benefits['age 65'] + (benefits['age 65']* 0.08))
        benefits['age 67'] = round(benefits['age 66'] + (benefits['age 66']* 0.08))
        benefits['age 68'] = round(benefits['age 67'] + (benefits['age 67']* 0.08))
        benefits['age 69'] = round(benefits['age 68'] + (benefits['age 68']* 0.08))
    elif benefits['age 66']:
        benefits['age 67'] = round(benefits['age 66'] + (benefits['age 66']* 0.08))
        benefits['age 68'] = round(benefits['age 67'] + (benefits['age 67']* 0.08))
        benefits['age 69'] = round(benefits['age 68'] + (benefits['age 68']* 0.08))
    elif benefits['age 67']:
        benefits['age 68'] = round(benefits['age 67'] + (benefits['age 67']* 0.08))
        benefits['age 69'] = round(benefits['age 68'] + (benefits['age 68']* 0.08))
    if base == 'age 62':
        step = benefits[base]
        bump = 0.11
        for age in years[1:]:
            if benefits[age]:
                break
            else:
                benefits[age] = round( step + (step*bump) )
                bump = bump - 0.01
                step = benefits[age]
        return benefits
    return benefits

# sample params
params = {
    'dobmon': 8,
    'dobday': 8,
    'yob': 1958,
    'earnings': 30000,
    'lastYearEarn': '',# possible use for unemployed or already retired
    'lastEarn': '',# possible use for unemployed or already retired
    'retiremonth': '',# leve blank to get triple calculation -- 62, 67 and 70
    'retireyear': '',# leve blank to get triple calculation -- 62, 67 and 70
    'dollars': 1,# benefits to be calculated in current-year dollars
    'prgf': 2
}
def get_retire_data(params):
    starter = datetime.datetime.now()
    collector = {}
    results = {'data': {
                    'early retirement age': '', 
                    'full retirement age': '', 
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
                        },
                    'params': params,
                    'disability': '',
                    'survivor benefits': {
                                    'child': '',
                                    'spouse caring for child': '',
                                    'spouse at full retirement age': '',
                                    'family maximum': ''
                                    }
                    },
                'error': ''
              }
    too_old = past_fra_test("%s-%s-%s" % (params['yob'], params['dobmon'], params['dobday']))
    # if too_old == 'invalid birth year':
    #     results['error'] = "Can't calculate retirement date from given birth year"
    #     return json.dumps(results)
    # if too_old == 'too young to calculate benefits':
    #     results['error'] = "Subject is too young to calculate benefits"
    #     return json.dumps(results)
    if too_old == True:
        results['error'] = "Subject is already past full retirement age"
        # TODO: handle special case
        return json.dumps(results)
    req = requests.post(result_url, data=params)
    if req.reason != 'OK':
        results['error'] = "request to Social Security failed: %s %s" % (req.reason, req.status_code)
        print results['error']
        return json.dumps(results)
    else:
        fra_tuple = get_retirement_age(params['yob'])
        soup = bs(req.text)
        tables = soup.findAll('table', {'bordercolor': '#6699ff'})
        results_table = tables[1]
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

        results['data']:
            'early retirement age': '', 
            'full retirement age': '', 
            'benefits': {
                'age 62': 0, 

        """
        BENS = results['data']['benefits']
        for key in collector:
            bits = key.split(' in ')
            retire_age_all = bits[0]
            retire_age_year = bits[0].split()[0]
            retire_year = bits[1]
            benefit_raw = collector[key]
            try:
                benefit = int(benefit_raw.split('.')[0].replace(',', '').replace('$', ''))
            except:
                benefit = 0
            if retire_age_year == str(fra_tuple[0]):
                results['data']['full retirement age'] = retire_age_all
                BENS['age %s' % retire_age_year] = benefit
            if retire_age_year == '62':
                results['data']['early retirement age'] = retire_age_all
                BENS['age %s' % retire_age_year] = benefit
            if retire_age_year == '70':
                BENS['age %s' % retire_age_year] = benefit
        additions = interpolate_benefits(BENS)
        for key in BENS:
            if additions[key] and not BENS[key]:
                BENS[key] = additions[key]

        # TODO: finish interpolations for any gap years
        jout = json.dumps(results)
        # with open('ssa.json', 'w') as f:
        #     f.write(jout)
        print "script took %s to run" % (datetime.datetime.now() - starter)
        return jout

        ## park detail scraper until indexing data is needed 
        # raw_comments = comment.findall(req.text)
        # comments = [clean_comment(com) for com in raw_comments if clean_comment(com) and not clean_comment(com).startswith('Indexed') and not clean_comment(com).startswith('Nominal')]
        # headings = [term.strip() for term in comments[0].split()]
        # headings.pop(headings.index('max'))
        # headings[headings.index('Tax')] = 'Tax_max'
        # detail_rows = []
        # details = []
        # for row in comments[1:]:
        #     if num_test(row.split()[0]):
        #         detail_rows.append([cell.strip() for cell in row.split()])
        #     else:
        #         details.append(row)
        # for row in detail_rows:
        #     results['earnings_data'].append({tup[0]: tup[1] for tup in zip(headings, row)})
        # results['benefit_details']['family_max'] = details.pop(-1)
        # results['benefit_details']['indexing']={}
        # INDEXING = results['benefit_details']['indexing']
        # sets = len(details) / 3
        # i1, i2 = (-3, 0)
        # for i in range(sets):
        #     i1 += 3
        #     i2 += 3
        #     INDEXING.update(parse_details(details[i1:i2]))

