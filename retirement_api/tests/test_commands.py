import mock
import unittest

from django.core.management.base import CommandError
from django.core.management import call_command

from retirement_api.management.commands import check_ssa_values, check_ssa
from retirement_api.utils.check_api import collector


class CommandTests(unittest.TestCase):
    @mock.patch('retirement_api.management.commands.check_ssa_values.ssa_check.run_tests')
    def test_check_ssa_values(self, mock_run_tests):
        mock_run_tests.return_value = 'OK'
        test_run = call_command('check_ssa_values')
        self.assertTrue(mock_run_tests.call_count == 1)
        test_run2 = call_command('check_ssa_values',
                                 '--recalibrate')
        self.assertTrue(mock_run_tests.call_count == 2)
        # mock_run_tests.return_value = 'Mismatches'
        # with self.assertRaises(CommandError):
        #     call_command('check_ssa_values')

    @mock.patch('retirement_api.management.commands.check_ssa.check_api.run')
    def test_check_ssa(self, mock_run):
        mock_run.return_value = collector
        test_run = call_command('check_ssa')
        self.assertTrue(mock_run.call_count == 1)
