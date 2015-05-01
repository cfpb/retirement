import os
import sys
from retirement_api.models import AgeChoice, Question

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class ViewModels(TestCase):

    testcase = AgeChoice.objects.get(age=67)

    def setUp(self):
        testquestion = Question(title='test q')
        testquestion.save()

    def test_get_subhed(self):
        self.assertTrue("You've chosen age 67" in self.testcase.get_subhed())

    def test_question_slug(self):
        tq = Question.objects.get(title='test q')
        self.assertTrue(tq.slug == "test_q")

