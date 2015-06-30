import os
import sys
import math
# import sys
import json
import datetime
from dateutil import parser

TODAY = datetime.datetime.now().date()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)

from retirement_api.models import ErrorText
# from ..models import ErrorText

TOO_YOUNG = ErrorText.objects.get(slug='too_young').note
TOO_OLD = ErrorText.objects.get(slug='too_old').note
# TOO_YOUNG = """\
# We're sorry. Our tool cannot provide an estimate \
# if you not at least 22 years old. Please visit the \
# Social Security Administration's \
# <a href="http://www.ssa.gov/people/youngpeople/" \
# target="blank">advice page</a> for students and younger workers.\
# """
# TOO_OLD = """\
# We're sorry. We cannot provide an estimate because you are older than \
# Social Security's maximum claiming age. To check your benefits, contact \
# the Social Security Administration or open a \
# <a href="http://www.socialsecurity.gov/myaccount/" target="_blank">\
# my Social Security</a> account.\
# """

# this datafile specifies years that have unique retirement age values
# since this may change, it is maintained in the repo
datafile = "%s/retirement_api/data/unique_retirement_ages_%s.json" % (BASE_DIR, TODAY.year)
with open(datafile, 'r') as f:
    age_map = json.loads(f.read())
    for year in age_map:
        age_map[year] = tuple(age_map[year])


def get_current_age(dob):
    today = datetime.date.today()
    try:
        DOB = parser.parse(dob).date()
    except:
        return None
    else:
        if DOB and DOB < today:
            try:  # when dob is 2/29 and the current year is not a leap year
                birthday = DOB.replace(year=today.year)
            except ValueError:
                birthday = DOB.replace(year=today.year, day=DOB.day-1)
            if birthday > today:
                return today.year - DOB.year - 1
            else:
                return today.year - DOB.year
        else:
            return None


def yob_test(yob=None):
    """
    tests to make sure suppied birth year is valid;
    returns valid birth year as a string or None
    """
    today = datetime.datetime.now().date()
    if not yob:
        return None
    try:
        birth_year = int(yob)
    except:
        print "birth year should be a number"
        return None
    else:
        b_string = str(birth_year)
        if birth_year > today.year:
            print "can't work with birth dates in the future"
            return None
        elif len(b_string) != 4:
            print "please supply a 4-digit birth year"
            return None
        else:
            return b_string


def get_retirement_age(birth_year):
    """
    given a worker's birth year,
    returns full retirement age in years and months;
    returns None if the supplied year isn't valid
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if b_string in age_map.keys():
            return age_map[b_string]
        elif yob <= 1937:
            return (65, 0)
        elif yob >= 1943 and yob <= 1954:
            return (66, 0)
        elif yob >= 1960:
            return (67, 0)
    else:
        return None


def past_fra_test(dob=None):
    """
    tests whether a person is past his/her full retirement age
    """
    if not dob:
        return 'invalid birth year entered'
    DOB = parser.parse(dob).date()
    today = datetime.datetime.now().date()
    current_age = get_current_age(dob)
    if DOB >= today:
        return 'invalid birth year entered'
    # SSA has a special rule for people born on Jan. 1
    # http://www.socialsecurity.gov/OACT/ProgData/nra.html
    if DOB.month == 1 and DOB.day == 1:
        fra_tuple = get_retirement_age(DOB.year-1)
    else:
        fra_tuple = get_retirement_age(DOB.year)
    if not fra_tuple:
        return 'invalid birth year entered'
    fra_year = fra_tuple[0]
    fra_month = fra_tuple[1]
    months_at_birth = DOB.year*12 + DOB.month - 1
    months_today = today.year*12 + today.month - 1
    delta = months_today - months_at_birth
    age_tuple = (current_age, (delta % 12))
    print "age_tuple: %s; fra_tuple: %s" % (age_tuple, fra_tuple)
    if age_tuple[0] < 22:
        return TOO_YOUNG
    if age_tuple[0] > 70:
        return TOO_OLD
    if age_tuple[0] > fra_tuple[0]:
        return True
    elif age_tuple[0] < fra_tuple[0]:
        return False
    elif age_tuple[0] == fra_tuple[0] and age_tuple[1] >= fra_tuple[1]:
        return True
    else:
        return False


def get_delay_bonus(birth_year):
    """
    given a worker's year of birth,
    returns the annual bonus for delaying retirement
    past full retirement age
    """
    b_string = yob_test(birth_year)
    if b_string:
        yob = int(birth_year)
        if yob in [1933, 1934]:
            return 5.5
        elif yob in [1935, 1936]:
            return 6.0
        elif yob in [1937, 1938]:
            return 6.5
        elif yob in [1939, 1940]:
            return 7.0
        elif yob in [1941, 1942]:
            return 7.5
        elif yob >= 1943:
            return 8.0
        else:
            return None
