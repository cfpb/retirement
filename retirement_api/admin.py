#!/usr/bin/env python
from django.contrib import admin
from retirement_api.models import (Page, Question, Step,
                                   Calibration, AgeChoice, Tooltip)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'h1', 'intro')


class AgeChoiceAdmin(admin.ModelAdmin):
    list_display = ('age', 'aside')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'workflow_state')


class TooltipAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')

admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Step)
admin.site.register(AgeChoice, AgeChoiceAdmin)
admin.site.register(Tooltip, TooltipAdmin)
admin.site.register(Calibration)
