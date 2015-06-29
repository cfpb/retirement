#!/usr/bin/env python
from django.contrib import admin
from retirement_api.models import Page, Question, Step, AgeChoice, Tooltip, ErrorText


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'h1', 'intro')


class AgeChoiceAdmin(admin.ModelAdmin):
    list_display = ('age', 'aside')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'question', 'workflow_state')


class TooltipAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')


class ErrorTextAdmin(admin.ModelAdmin):
    list_display = ('slug', 'error', 'note', 'internal_note')

admin.site.register(Page, PageAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Step)
admin.site.register(AgeChoice, AgeChoiceAdmin)
admin.site.register(Tooltip, TooltipAdmin)
admin.site.register(ErrorText, ErrorTextAdmin)
