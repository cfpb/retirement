from django.db import models
from django.template.defaultfilters import slugify

WORKFLOW_STATE = [
    ('APPROVED', 'Approved'),
    ('REVISED', 'Revised'),
    ('SUBMITTED', 'Submitted'),
]

class Step(models.Model):
    title = models.CharField(max_length=500)
    instructions = models.TextField(max_length=255, blank=True)
    note = models.TextField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title

class AgeChoice(models.Model):
    age = models.IntegerField()
    aside = models.CharField(max_length=500)

    def get_subhed(self):
        return "You've chosen age %s. %s Here are some steps \
                to help you in the next few years." % (self.age, self.aside)
    class Meta:
        ordering = ['age']

class Page(models.Model):
    title = models.CharField(max_length=255)
    h1 = models.CharField(max_length=255, blank=True)
    intro = models.TextField(max_length=255)
    h2 = models.CharField(max_length=255, blank=True)
    h3 = models.CharField(max_length=255, blank=True)
    h4 = models.CharField(max_length=255, blank=True)
    step1 = models.ForeignKey(Step, related_name='step1', blank=True, null=True)
    step2 = models.ForeignKey(Step, related_name='step2', blank=True, null=True)
    step3 = models.ForeignKey(Step, related_name='step3', blank=True, null=True)
    final_steps = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

class Tooltip(models.Model):
    title = models.CharField(max_length=500)
    text = models.TextField(max_length=255, blank=True)

    def __unicode__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(blank=True)
    question = models.TextField(blank=True)
    answer_yes_a_subhed = models.CharField(max_length=255, blank=True, help_text="Under 50")
    answer_yes_a = models.TextField(blank=True, help_text="Under 50")
    answer_yes_b_subhed = models.CharField(max_length=255, blank=True, help_text="50 and older")
    answer_yes_b = models.TextField(blank=True, help_text="50 and older")
    answer_no_a_subhed = models.CharField(max_length=255, blank=True, help_text="Under 50")
    answer_no_a = models.TextField(blank=True, help_text="Under 50")
    answer_no_b_subhed = models.CharField(max_length=255, blank=True, help_text="50 and older")
    answer_no_b = models.TextField(blank=True, help_text="50 and older")
    answer_unsure_a_subhed = models.CharField(max_length=255, blank=True, help_text="Under 50")
    answer_unsure_a = models.TextField(blank=True, help_text="Under 50")
    answer_unsure_b_subhed = models.CharField(max_length=255, blank=True, help_text="50 and older")
    answer_unsure_b = models.TextField(blank=True, help_text="50 and older")
    workflow_state = models.CharField(
        max_length=255, choices=WORKFLOW_STATE, default='SUBMITTED')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).replace('-', '_')
        super(Question, self).save(*args, **kwargs)
