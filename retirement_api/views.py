import datetime
import json
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import activate, deactivate_all, ugettext as _

from dateutil import parser

from retirement_api.models import AgeChoice, Page, Question, Step, Tooltip

from .utils.ss_calculator import get_retire_data
from .utils.ss_utilities import get_retirement_age


BASEDIR = os.path.dirname(__file__)

standalone = getattr(settings, "STANDALONE", False)

if standalone:
    base_template = "retirement_api/standalone/base_update.html"
else:  # pragma: no cover
    base_template = "front/base_update.html"


def claiming(request, es=False):
    if es is True:
        activate("es")
        language = "es"
    else:
        language = "en"
        deactivate_all()
    ages = {}
    for age in AgeChoice.objects.all():
        ages[age.age] = _(age.aside)
    page = Page.objects.get(title="Planning your Social Security claiming age")
    tips = {}
    for tooltip in Tooltip.objects.all():
        tips[tooltip.title] = tooltip.text
    questions = {}
    for q in Question.objects.all():
        questions[q.slug] = q
    steps = {}
    for step in Step.objects.all():
        steps[step.title] = step.trans_instructions(language=language)

    cdict = {
        "tstamp": datetime.datetime.now(),
        "steps": steps,
        "questions": questions,
        "tips": tips,
        "ages": ages,
        "page": page,
        "base_template": base_template,
        "available_languages": ["en", "es"],
        "es": es,
        "language": language,
        "about_view_name": "retirement_api:" + ("about_es" if es else "about"),
    }

    return render(request, "retirement_api/claiming.html", cdict)


def param_check(request, param):
    if param in request.GET and request.GET[param]:
        return request.GET[param]
    else:
        return None


def income_check(param):
    cleaned = param.replace("$", "").replace(",", "").partition(".")[0]
    try:
        clean_income = int(cleaned)
    except ValueError:
        return None
    else:
        return clean_income


def estimator(request, dob=None, income=None, language="en"):
    ssa_params = {
        "dobmon": 0,
        "dobday": 0,
        "yob": 0,
        "earnings": 0,
        "lastYearEarn": "",  # not using
        "lastEarn": "",  # not using
        "retiremonth": "",  # only using for past-FRA users
        "retireyear": "",  # only using for past-FRA users
        "dollars": 1,  # benefits to be calculated in current-year dollars
        "prgf": 2,
    }
    if dob is None:
        dob = param_check(request, "dob")
        if not dob:
            return HttpResponseBadRequest("invalid date of birth")
    if income is None:
        income_raw = param_check(request, "income")
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
    except ValueError:
        return HttpResponseBadRequest("invalid date of birth")
    else:
        DOB = dob_parsed.date()
    ssa_params["dobmon"] = DOB.month
    ssa_params["dobday"] = DOB.day
    ssa_params["yob"] = DOB.year
    ssa_params["earnings"] = income
    data = get_retire_data(ssa_params, language)
    return HttpResponse(json.dumps(data), content_type="application/json")


def get_full_retirement_age(request, birth_year):
    data_tuple = get_retirement_age(birth_year)
    if not data_tuple:
        return HttpResponseBadRequest("bad birth year (%s)" % birth_year)
    else:
        data = json.dumps(data_tuple)
        return HttpResponse(data, content_type="application/json")


def about(request, language="en"):
    """Return our 'about' calculation-explainer page in Engish or Spanish"""
    if language == "es":
        activate("es")
        es = True
    else:
        deactivate_all()
        es = False
    cdict = {
        "base_template": base_template,
        "available_languages": ["en", "es"],
        "es": es,
    }
    return render(request, "retirement_api/about.html", cdict)
