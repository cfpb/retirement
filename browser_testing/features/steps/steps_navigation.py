# coding: utf-8
from behave import given, when, then
from hamcrest.core import assert_that, equal_to
from hamcrest.library.text.stringcontains import contains_string
from decorators import *

from pages.home import Home
from pages.base import Base
from pages.utils import Utils

# XPATH LOCATORS

# RELATIVE URL'S
HOME = 'index.html'


@given(u'I navigate to the Retirement landing page')
@handle_error
def step(context):
    context.base.go('retirement/before-you-claim')


# @then(u'I should see "{link_name}" displayed in the page title')
# @handle_error
# def step(context, link_name):
#     # Verify that the page title matches the link we clicked
#     page_title = context.base.get_page_title()
#     assert_that(page_title, contains_string(link_name))


@given(u'I enter birth and salary info')
@handle_error
def step(context):
    context.base.enter_month('07')
    context.base.enter_day('07')
    context.base.enter_year('1970')
    context.base.enter_income('70000')
    context.base.get_estimate()
    Utils().zzz(1)

@when(u'I click on the "{link_name}" link')
@handle_error
def step(context, link_name):
    context.base.click_link(link_name)
    Utils().zzz(2)


@then(u'I should see the "{relative_url}" URL with page title "{page_title}"')
@handle_error
def step(context, relative_url, page_title):
    current_page_title = context.base.get_blank_handle_title()
    assert_that(current_page_title, contains_string(page_title))

    actual_url = context.base.get_blank_handle_url()
    assert_that(actual_url, contains_string(relative_url))
