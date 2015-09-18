import os
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from utils.ss_calculator import get_retire_data, params
from utils.ss_utilities import get_retirement_age
from dateutil import parser
import datetime
from retirement_api.models import Step, AgeChoice, Page, Tooltip, Question
from django.utils.translation import ugettext as _
from django.utils.translation import activate, deactivate_all
BASEDIR = os.path.dirname(__file__)

try:
    import settings
    standalone = settings.STANDALONE
except:  # pragma: no cover
    standalone = False

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
    if es is True:
        activate('es')
    else:
        deactivate_all()
    ages = {}
    for age in AgeChoice.objects.all():
        ages[age.age] = _(age.aside)
    page = Page.objects.get(title='Before You Claim')
    tips = {}
    for tooltip in Tooltip.objects.all():
        tips[tooltip.title] = tooltip.text
    questions = {}
    for q in Question.objects.all():
        questions[q.slug] = q
    final_steps = {}
    for step in Step.objects.filter(title__contains='final_'):
        final_steps[step.title] = step
    if standalone:
        base_template = "standalone_base.html"
    else:
        base_template = "%s/templates/base.html" % BASEDIR
    cdict = {
        'tstamp': datetime.datetime.now(),
        'final_steps': final_steps,
        'questions': questions,
        'tips': tips,
        'ages': ages,
        'page': page,
        'base_template': base_template,
        'available_languages': ['en', 'es'],
        'es': es,
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


def estimator(request, dob=None, income=None, language='en'):
    today = datetime.datetime.now().date()
    legal_year = today.year - 22  # calculator isn't for people under 22
    if dob is None:
        dob = param_check(request, 'dob')
        if not dob:
            return HttpResponseBadRequest("invalid date of birth")
    if income is None:
        income_raw = param_check(request, 'income')
        if not income_raw:
            return HttpResponseBadRequest("invalid income")
        else:
            income = income_check(income_raw)
            if income is None:
                return HttpResponseBadRequest("invalid income")
    else:
        income = income_check(income)
        if income is None:
            return HttpResponseBadRequest("invalid income")
    try:
        dob_parsed = parser.parse(dob)
    except:
        return HttpResponseBadRequest("invalid date of birth")
    else:
        DOB = dob_parsed.date()
    params['dobmon'] = DOB.month
    params['dobday'] = DOB.day
    params['yob'] = DOB.year
    params['earnings'] = income
    data = get_retire_data(params, language)
    return HttpResponse(data, content_type='application/json')


def get_full_retirement_age(request, birth_year):
    data_tuple = get_retirement_age(birth_year)
    if not data_tuple:
        return HttpResponseBadRequest("bad birth year (%s)" % birth_year)
    else:
        data = json.dumps(data_tuple)
        return HttpResponse(data, content_type='application/json')
