from behave import given, when, then
from hamcrest.core import assert_that
from hamcrest.core.core.isequal import equal_to
from decorators import *

from pages.home import Home
from pages.base import Base


# Choose age
@when(u'I Choose age "{age}"')
@handle_error
def step(context, age):
    context.base.choose_age(age)

