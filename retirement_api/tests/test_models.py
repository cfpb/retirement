import os
import sys
from retirement_api.models import AgeChoice, Question, Step, Page, Tooltip
import mock

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")


class ViewModels(TestCase):

    testagechoice = AgeChoice(age=62, aside="Aside.")
    testquestion = Question(title="Test Question", slug='')
    teststep = Step(title="Test Step")
    testpage = Page(title="Page title", intro="Intro")
    testtip = Tooltip(title="Test Tooltip")

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

    def test_quesiton_dump(self):
        dumplist = self.testquestion.dump_translation_text()
        self.assertTrue(type(dumplist) == list)
        # outfile = "/tmp/%s.po" % self.testquestion.slug
        # self.testquestion.dump_translation_text(output=True)
        # self.assertTrue(os.path.isfile(outfile))

    def test_question_dump_mock_output(self):
        open_name = '%s.open' % __name__
        with mock.patch(open_name, create=True) as mock_open:
            mock_open.return_value = mock.MagicMock(spec=file)
            self.testquestion.dump_translation_text(output=True)
            file_handle = mock_open.return_value.__enter__.return_value
            file_handle.write.assert_call_count == 5

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
