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

from bs4 import BeautifulSoup as bs

# sample minimal form data needed
yob = 1956
mob = 8
dayob = 14
earnings = 50000

base_url = "http://www.ssa.gov"
quick_url = "%s/OACT/quickcalc/" % base_url# where users go, but not needed for our request
result_url = "%s/cgi-bin/benefit6.cgi" % base_url
params = {
    'dobmon': mob,
    'dobday': dayob,
    'yob': yob,
    'earnings': earnings,
    'lastYearEarn': '',# possible use for unemployed or already retired
    'lastEarn': '',# possible use for unemployed or already retired
    'retiremonth': '',# leve blank to get triple calculation -- 62, 67 and 70
    'retireyear': '',# leve blank to get triple calculation -- 62, 67 and 70
    'dollars': 1,# benefits to be calculated in current-year dollars
    'prgf': 2
}

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

def parse_details(rows):
    datad = {}
    if len(rows) == 3:
        titlerow = rows[0].split(':')
        datad[titlerow[0].strip().upper()] = {'Bend points': titlerow[1].strip()}
        outer = datad[titlerow[0].strip().upper()]
        outer['AIME']  = rows[1]
        outer['COLA'] = rows[2]
    return datad

def get_retire_data(params):
    starter = datetime.datetime.now()
    results = {'benefits': {}, 'earnings_data': [], 'benefit_details': {}, 'params': params}
    req = requests.post(result_url, data=params)
    if req.reason != 'OK':
        print "request to SS failed: %s %s" % (req.reason, req.status_code)
        return results
    else:
        soup = bs(req.text)
        if params['retiremonth'] and params['retireyear']:
            ret_age = soup.find(id='ret_age').text.strip()
            ret_year = soup.find(id='ret_date').text.strip()
            ret_amt = soup.find(id='ret_amount').text.replace(',', '').partition('.')[0]
            results['benefits']['%s in %s' % (ret_age, ret_year)] = int(ret_amt)
        else:
            tables = soup.findAll('table', {'bordercolor': '#6699ff'})
            results_table = tables[1]
            result_rows = results_table.findAll('tr')
            for row in result_rows:
                cells = row.findAll('td')
                if cells:
                    results['benefits'][cells[0].text] = cells[1].text

        # detail data
        raw_comments = comment.findall(req.text)
        comments = [clean_comment(com) for com in raw_comments if clean_comment(com) and not clean_comment(com).startswith('Indexed') and not clean_comment(com).startswith('Nominal')]
        headings = [term.strip() for term in comments[0].split()]
        headings.pop(headings.index('max'))
        headings[headings.index('Tax')] = 'Tax_max'
        detail_rows = []
        details = []
        for row in comments[1:]:
            if num_test(row.split()[0]):
                detail_rows.append([cell.strip() for cell in row.split()])
            else:
                details.append(row)
        for row in detail_rows:
            results['earnings_data'].append({tup[0]: tup[1] for tup in zip(headings, row)})
        results['benefit_details']['family_max'] = details.pop(-1)
        results['benefit_details']['indexing']={}
        INDEXING = results['benefit_details']['indexing']
        sets = len(details) / 3
        i1, i2 = (-3, 0)
        for i in range(sets):
            i1 += 3
            i2 += 3
            INDEXING.update(parse_details(details[i1:i2]))
        # print "exporting ssa.json"
        # jout = json.dumps(results)
        # with open('ssa.json', 'w') as f:
        #     f.write(jout)
        print "script took %s to run" % (datetime.datetime.now() - starter)
        return jout

