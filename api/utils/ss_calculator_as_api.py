"""
experimenting with SS quick-calculator page as trial api for demo pages

users must be at least 22 to use the form

Well need to ask user for DOB and current annual earnings
we'll return estimated benefits at 62, 67, and 70 based the value of the dollar today

inputs needed:
    Date of birth: 8/14/1957
    Current earnings: 70000

optional inputs:
    Last year with earnings # could be useful for users who are retired or unemployed
    Last earnings # ditto
    Retirement month/year: 8/2027) # feed won't return 3 retire options if we provide this
    Benefit in year-2015 dollars) # SS can take today's dollars (1) or future, inflated dollars (0)
"""

import re
import requests
import json

from bs4 import BeautifulSoup as bs

# sample minimal form data needed
yob = 1957
mob = 8
dayob = 14
earnings = 103000

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

def num_test(value):
    try:
        x = int(value)
    except:
        return False
    else:
        return True

def get_retire_data(params):
    results = {'summary_data': {}, 'detail_data': [], 'detail_notes': = {}}
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
            results['summary_data']['%s in %s' % (ret_age, ret_year)] = int(ret_amt)
        else:
            tables = soup.findAll('table', {'bordercolor': '#6699ff'})
            results_table = tables[1]
            result_rows = results_table.findAll('tr')
            for row in result_rows:
                cells = row.findAll('td')
                if cells:
                    results['summary_data'][cells[0].text] = cells[1].text

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
            results['detail_data'].append({tup[0]: tup[1] for tup in zip(headings, row)})
        results['detail_notes']['family_note'] = details.pop(-1)
        items = iter(details)
        results['detail_notes'][items.next()] = [items.next(), items.next()]
        with open('ssa.json', 'w') as f:
            f.write(json.dumps(results))

