# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Step'
        db.create_table(u'retirement_api_step', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('instructions', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'retirement_api', ['Step'])

        # Adding model 'AgeChoice'
        db.create_table(u'retirement_api_agechoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')()),
            ('aside', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'retirement_api', ['AgeChoice'])

        # Adding model 'Page'
        db.create_table(u'retirement_api_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('h1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('intro', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('h2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('h3', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('h4', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('step1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='step1', null=True, to=orm['retirement_api.Step'])),
            ('step2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='step2', null=True, to=orm['retirement_api.Step'])),
            ('step3', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='step3', null=True, to=orm['retirement_api.Step'])),
            ('final_steps', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'retirement_api', ['Page'])

        # Adding model 'Tooltip'
        db.create_table(u'retirement_api_tooltip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'retirement_api', ['Tooltip'])

        # Adding model 'Question'
        db.create_table(u'retirement_api_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('question', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_yes_a_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_yes_a', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_yes_b_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_yes_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_no_a_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_no_a', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_no_b_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_no_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_unsure_a_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_unsure_a', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('answer_unsure_b_subhed', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('answer_unsure_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('workflow_state', self.gf('django.db.models.fields.CharField')(default='SUBMITTED', max_length=255)),
        ))
        db.send_create_signal(u'retirement_api', ['Question'])


    def backwards(self, orm):
        # Deleting model 'Step'
        db.delete_table(u'retirement_api_step')

        # Deleting model 'AgeChoice'
        db.delete_table(u'retirement_api_agechoice')

        # Deleting model 'Page'
        db.delete_table(u'retirement_api_page')

        # Deleting model 'Tooltip'
        db.delete_table(u'retirement_api_tooltip')

        # Deleting model 'Question'
        db.delete_table(u'retirement_api_question')


    models = {
        u'retirement_api.agechoice': {
            'Meta': {'ordering': "['age']", 'object_name': 'AgeChoice'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'aside': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'retirement_api.page': {
            'Meta': {'object_name': 'Page'},
            'final_steps': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'h1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'h2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'h3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'h4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'step1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'step1'", 'null': 'True', 'to': u"orm['retirement_api.Step']"}),
            'step2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'step2'", 'null': 'True', 'to': u"orm['retirement_api.Step']"}),
            'step3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'step3'", 'null': 'True', 'to': u"orm['retirement_api.Step']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'retirement_api.question': {
            'Meta': {'object_name': 'Question'},
            'answer_no_a': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_no_a_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'answer_no_b': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_no_b_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'answer_unsure_a': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_unsure_a_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'answer_unsure_b': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_unsure_b_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'answer_yes_a': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_yes_a_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'answer_yes_b': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'answer_yes_b_subhed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'workflow_state': ('django.db.models.fields.CharField', [], {'default': "'SUBMITTED'", 'max_length': '255'})
        },
        u'retirement_api.step': {
            'Meta': {'object_name': 'Step'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'retirement_api.tooltip': {
            'Meta': {'object_name': 'Tooltip'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['retirement_api']