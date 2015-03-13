import os
import sys
import datetime
import json
import csv

import requests
# from django.template.defaultfilters import slugify
from bs4 import BeautifulSoup as bs

TODAY = datetime.datetime.now().date()
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

data_dir = "%s/data" % BASE_DIR
backup_dir = "%s/data/backups" % BASE_DIR

ss_table_urls = {
    'cola': "http://www.socialsecurity.gov/OACT/COLA/colaseries.html",
    'actuarial_life': "http://www.socialsecurity.gov/OACT/STATS/table4c6.html",
    'retirement_ages': "http://www.socialsecurity.gov/OACT/ProgData/nra.html",# handled by get_retirement_age()
    'delay_credits': "http://www.socialsecurity.gov/retire2/delayret.htm",
}

def output_csv(filepath, headings, bs_rows):
    with open(filepath, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headings)
        for row in bs_rows:
            writer.writerow([cell.text.replace(',', '').strip() for cell in row.findAll('td') if row.findAll('td')])

def output_json(filepath, headings, bs_rows):
    with open(filepath, 'w') as f:
        json_out = {}
        for row in bs_rows:
            cells = [cell.text.replace(',', '').strip() for cell in row.findAll('td') if row.findAll('td')]
            if len(cells) == 2:
                json_out[cells[0]] = cells[1]
            else:
                tups = zip(headings[1:], cells[1:])
                json_out[cells[0]] = {tup[0]: tup[1] for tup in tups}
        f.write(json.dumps(json_out))

def update_cola():
    url = ss_table_urls['cola']
    outcsv = "%s/ss_cola_%s.csv" % (data_dir, TODAY.year)
    outjson = "%s/ss_cola_%s.json" % (data_dir, TODAY.year)
    headings = ['Year', 'COLA']
    req = requests.get(url)
    if req.reason != 'OK':
        print "request to %s failed: %s %s" % (url, req.status_code, req.reason)
    else:
        soup = bs(req.text)
        [s.extract() for s in soup('small')]
        tables = soup.findAll('table')[-3:]
    rows = []
    print "found %s tables" % len(tables)
    for table in tables:
        rows.extend([row for row in table.findAll('tr') if row.findAll('td')])
    output_csv(outcsv, headings, rows)
    print "updated %s with %s rows" % (outcsv, len(rows))
    output_json(outjson, headings, rows)
    print "updated %s with %s entries" % (outjson, len(rows))
        # else:
        #     print "didn't find more than 30 rows at %s" % url

def update_life():
    url = ss_table_urls['actuarial_life']
    outcsv = "%s/actuarial_life_%s.csv" % (data_dir, TODAY.year)
    outjson = "%s/actuarial_life_%s.json" % (data_dir, TODAY.year)
    headings = [
        'exact_age',
        'male_death_probability',
        'male_number_of_lives',
        'male_life_expectancy',
        'female_death_probability',
        'female_number_of_lives',
        'female_life_expectancy',
    ]
    req = requests.get(url)
    if req.reason != 'OK':
        print "request to %s failed: %s %s" % (url, req.status_code, req.reason)
    else:
        soup = bs(req.text)
        table = soup.find('table').find('table')
        if not table:
            print "couldn't find table at %s" % url
        else:
            rows = table.findAll('tr')[2:]
            if len(rows) > 100:
                output_csv(outcsv, headings, rows)
                print "updated %s with %s rows" % (outcsv, len(rows))
                output_json(outjson, headings, rows)
                print "updated %s with %s entries" % (outjson, len(rows))
            else:
                print "didn't find more than 100 rows at %s" % url

# if __name__ == "__main__":
#     update_life(ss_table_urls['actuarial_life'], update=True)
#     update_cola(ss_table_urls['cola'], update=True)
