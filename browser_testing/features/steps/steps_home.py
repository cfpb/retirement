from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from hamcrest.library.text.stringcontains import contains_string
from decorators import *

from pages.home import Home
from pages.base import Base

# import datetime
# timestamp = datetime.datetime.now()
# rolling dob to guarantee subject is 49 and full retirement age is 67
# dob = timestamp - datetime.timedelta(days=44*365+30)
# month = dob.month
# day = dob.day
# year = dob.year


# choose month
@when(u'I enter month "{month}"')
@handle_error
def step(context, month):
    context.base.enter_month(month)


# choose day
@when(u'I enter day "{day}"')
@handle_error
def step(context, day):
    context.base.enter_day(day)


# choose year
@when(u'I enter year "{year}"')
@handle_error
def step(context, year):
    context.base.enter_year(year)


# choose income
@when(u'I enter income "{income}"')
@handle_error
def step(context, income):
    context.base.enter_income(income)


# Choose age
@when(u'I click get estimate')
@handle_error
def step(context):
    context.base.get_estimate()


@when(u'I choose retirement age "{retirement_age}"')
@handle_error
def step(context, retirement_age):
    result = context.base.choose_retirement_age(retirement_age)


@then(u'I should see "{retirement_age}" in age_selector_response')
@handle_error
def step_impl(context, retirement_age):
    result = context.base.get_age_choice_result()
    assert_that(result, contains_string(retirement_age))


# see results in chart
@then(u'I should see result "{expected_result}" displayed in graph-container-text')
@handle_error
def step(context, expected_result):
    # Verify that the resulting retirement age appears in the chart
    result = context.base.get_fra_result()
    assert_that(result, contains_string(expected_result))
