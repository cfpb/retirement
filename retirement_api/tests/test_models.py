import os
import sys
import unittest
from retirement_api.models import AgeChoice, Question

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class ViewModels(unittest.TestCase):
    testcase = AgeChoice.objects.get(age=67)
    testquestion = Question(title='test q')

    def test_get_subhed(self):
        self.assertTrue("You've chosen age 67" in self.testcase.get_subhed())

    def test_question_slug(self):
        self.testquestion.save()
        self.assertTrue(self.testquestion.slug == "test_q")
        self.testquestion.delete()

