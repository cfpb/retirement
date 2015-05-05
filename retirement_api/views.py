import json

from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from utils.ss_calculator import get_retire_data, params
from utils.ss_utilities import get_retirement_age
from dateutil import parser
import datetime
from retirement_api.models import Step, AgeChoice, Page, Tooltip, Question
from django.utils.translation import ugettext as _
from django.utils.translation import activate

today = datetime.datetime.now().date()
# params = {
#     'dobmon': mob,
#     'dobday': dayob,
#     'yob': yob,
#     'earnings': earnings,
#     'lastYearEarn': '',# possible use for unemployed or already retired
#     'lastEarn': '',# possible use for unemployed or already retired
#     'retiremonth': '',# leve blank to get triple calculation -- 62, 67 and 70
#     'retireyear': '',# leve blank to get triple calculation -- 62, 67 and 70
#     'dollars': 1,# benefits to be calculated in current-year dollars
#     'prgf': 2
# }

def claiming(request, es=False):
    if es == True:
        activate('es')
    ages = {}
    for age in AgeChoice.objects.all():
        ages[age.age] = _(age.aside)
    page = Page.objects.get(title='Choosing Social Security')
    tips = {}
    for tooltip in Tooltip.objects.all():
        tips[tooltip.title] = tooltip.text
    questions = {}
    for q in Question.objects.all():
        questions[q.slug] = q
    final_steps = {}
    for step in Step.objects.filter(title__contains='final_'):
        final_steps[step.title] = step
    cdict = {
        'tstamp': datetime.datetime.now(),
        'final_steps': final_steps,
        'questions': questions,
        'tips': tips,
        'ages': ages,
        'page': page,
        'available_languages': ['en', 'es'],
        }
    return render_to_response('claiming.html', cdict)

def param_check(request, param):
    if param in request.GET and request.GET[param]:
        return request.GET[param]
    else:
        return None

def income_check(param):
    cleaned = param.replace('$', '').replace(',', '').partition('.')[0]
    try:
        clean_income = int(cleaned)
    except:
        return None
    else:
        return clean_income

def estimator(request, dob=None, income=None):
    legal_year = today.year - 22 # calculator should not be used for people under 22
    if dob == None:
        dob = param_check(request, 'dob')
        if not dob:
            return HttpResponseBadRequest("invalid date of birth")
    if income == None:
        income_raw = param_check(request, 'income')
        if not income_raw:
            return HttpResponseBadRequest("invalid income")
        else:
            income = income_check(income_raw)
            if income == None:
                return HttpResponseBadRequest("invalid income")
    else:
        income = income_check(income)
        if income == None:
            return HttpResponseBadRequest("invalid income")
    try:
        dob_parsed = parser.parse(dob)
    except:
        return HttpResponseBadRequest("invalid date of birth")
    else:
        DOB = dob_parsed.date()
    if DOB == today:
        print "birth date can't be parsed"
        return HttpResponseBadRequest("birth date can't be parsed")
    elif DOB.year >= legal_year:
        print "subject is too young to use SSA quick calculator"
        return HttpResponseBadRequest("subject is too young to use SSA quick calculator")
    else:
        params['dobmon'] = DOB.month
        params['dobday'] = DOB.day
        params['yob'] = DOB.year
        params['earnings'] = income
        data = get_retire_data(params)
        return HttpResponse(data, content_type='application/json')

def get_full_retirement_age(request, birth_year):
    data_tuple = get_retirement_age(birth_year)
    if not data_tuple:
        return HttpResponseBadRequest("bad birth year provided: (%s)" % birth_year)
    else:
        data = json.dumps(data_tuple)
        return HttpResponse(data, content_type='application/json')
