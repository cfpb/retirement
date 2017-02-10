import os
import sys
import datetime
from retirement_api.models import (AgeChoice,
                                   Question,
                                   Step,
                                   Page,
                                   Tooltip,
                                   Calibration)
import mock
from mock import patch, mock_open

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class ViewModels(TestCase):

    testagechoice = AgeChoice(age=62, aside="Aside.")
    testquestion = Question(
        title="Test Question", slug='', question="Test question.")
    teststep = Step(title="Test Step")
    testpage = Page(title="Page title", intro="Intro")
    testtip = Tooltip(title="Test Tooltip")
    testcalibration = Calibration(created=datetime.datetime.now())

    def test_calibration(self):
        self.assertTrue('calibration' in self.testcalibration.__unicode__())

    def test_get_subhed(self):
        tc = self.testagechoice
        self.assertTrue("You've chosen age 62" in tc.get_subhed())

    def test_question_slug(self):
        self.testquestion.save()
        self.assertTrue(self.testquestion.slug != '')

    def test_question_translist(self):
        tlist = self.testquestion.translist()
        self.assertTrue(type(tlist) == list)
        for term in ['question',
                     'answer_yes_a',
                     'answer_no_b',
                     'answer_unsure_a_subhed']:
            self.assertTrue(term in tlist)

    def test_question_dump(self):
        m = mock_open()
        with patch("__builtin__.open", m, create=True):
            mock_open.return_value = mock.MagicMock(spec=file)
            self.testquestion.dump_translation_text(output=True)
        self.assertTrue(m.call_count == 1)

    def test_question_dump_no_output(self):
        dump = self.testquestion.dump_translation_text()
        self.assertEqual('Test question.', dump[0])

    def test_agechoice_translist(self):
        tlist = self.testagechoice.translist()
        self.assertTrue(type(tlist) == list)

    def test_step_translist(self):
        tlist = self.teststep.translist()
        self.assertTrue(type(tlist) == list)

    def test_page_translist(self):
        tlist = self.testpage.translist()
        self.assertTrue(type(tlist) == list)

    def test_tooltip_translist(self):
        tlist = self.testtip.translist()
        self.assertTrue(type(tlist) == list)
