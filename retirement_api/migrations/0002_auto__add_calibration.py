# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Calibration'
        db.create_table(u'retirement_api_calibration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('results_json', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'retirement_api', ['Calibration'])


    def backwards(self, orm):
        # Deleting model 'Calibration'
        db.delete_table(u'retirement_api_calibration')


    models = {
        u'retirement_api.agechoice': {
            'Meta': {'ordering': "['age']", 'object_name': 'AgeChoice'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'aside': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'retirement_api.calibration': {
            'Meta': {'object_name': 'Calibration'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results_json': ('django.db.models.fields.TextField', [], {})
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