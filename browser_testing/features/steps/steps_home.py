from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from decorators import *

from pages.home import Home
from pages.base import Base


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
def step(context, get_estimate):
    context.base.get_estimate()


# see results in chart
@then(u'I should see result "{expected_result}" displayed in graph-container-text')
@handle_error
def step(context, expected_result):
    # Verify that the resulting retirement age appears in the chart
    result = context.base.get_fra_result()
    assert_that(result, contains_string(expected_result))


@when(u'I Choose age "70"')
@handle_error
def step(context):
    result = context.base.choose_age_70()


@then(u'I should see "70" displayed in age_selector_response')
@handle_error
def step_impl(context):
    result = context.base.get_age_choice_result()
    assert_that(result, contains_string('expected_result'))
