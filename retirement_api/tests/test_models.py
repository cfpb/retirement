import os
import sys
from retirement_api.models import AgeChoice, Question

from django.test import TestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class ViewModels(TestCase):

    def setUp(self):
        testcase = AgeChoice.objects.get_or_create(age=61)
        testquestion = Question(title='test q')
        testquestion.save()

    def test_get_subhed(self):
        tc = AgeChoice.objects.get(age=61)
        self.assertTrue("You've chosen age 61" in tc.get_subhed())

    def test_question_slug(self):
        tq = Question.objects.get(title='test q')
        self.assertTrue(tq.slug == "test_q")

