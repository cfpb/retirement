import os
import sys
from retirement_api.models import AgeChoice, Question, Step, Page, Tooltip
import mock

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class ViewModels(TestCase):

    testcase = AgeChoice.objects.get(age=61)
    testquestion = Question.objects.all()[0]
    teststep = Step.objects.all()[0]
    testpage = Page.objects.all()[0]
    testtip = Tooltip.objects.all()[0]

    def test_get_subhed(self):
        tc = AgeChoice.objects.get(age=61)
        self.assertTrue("You've chosen age 61" in tc.get_subhed())

    def test_question_slug(self):
        question_slugger = Question(title='test q')
        question_slugger.save()
        self.assertTrue(question_slugger.slug == "test_q")
        question_slugger.delete()

    def test_question_translist(self):
        tlist = self.testquestion.translist()
        self.assertTrue(type(tlist) == list)
        for term in ['question', 'answer_yes_a', 'answer_no_b', 'answer_unsure_a_subhed']:
            self.assertTrue(term in tlist)

    def test_quesiton_dump(self):
        dumplist = self.testquestion.dump_translation_text()
        self.assertTrue(type(dumplist) == list)
        outfile = "/tmp/%s.po" % self.testquestion.slug
        self.testquestion.dump_translation_text(output=True)
        self.assertTrue(os.path.isfile(outfile))

    def test_agechoice_translist(self):
        tlist = self.testcase.translist()
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
