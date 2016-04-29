import sys
import os
import datetime
import json
import mock

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.test import TestCase
import unittest
from django.http import HttpRequest
from django.conf import settings

from retirement_api.management.commands import check_ssa_values

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class CommandTests(unittest.TestCase):

    @mock.patch('retirement_api.management.commands.check_ssa_values.ssa_check.run_tests')
    def test_check_ssa_values(self, mock_run_tests):
        mock_run_tests.return_value = 'OK'
        test_run = call_command('check_ssa_values')
        self.assertTrue(mock_run_tests.call_count == 1)
        test_run2 = call_command('check_ssa_values',
                                 '--recalibrate')
        self.assertTrue(mock_run_tests.call_count == 2)
