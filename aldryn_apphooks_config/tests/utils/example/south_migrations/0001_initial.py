# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExampleConfig'
        db.create_table(u'example_exampleconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=100)),
            ('app_data', self.gf('app_data.fields.AppDataField')(default='{}')),
            ('app_title', self.gf('django.db.models.fields.CharField')(max_length=234)),
        ))
        db.send_create_signal(u'example', ['ExampleConfig'])

        # Adding unique constraint on 'ExampleConfig', fields ['type', 'namespace']
        db.create_unique(u'example_exampleconfig', ['type', 'namespace'])

        # Adding model 'AnotherExampleConfig'
        db.create_table(u'example_anotherexampleconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('namespace', self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=100)),
            ('app_data', self.gf('app_data.fields.AppDataField')(default='{}')),
            ('max_entries', self.gf('django.db.models.fields.SmallIntegerField')(default=5)),
        ))
        db.send_create_signal(u'example', ['AnotherExampleConfig'])

        # Adding unique constraint on 'AnotherExampleConfig', fields ['type', 'namespace']
        db.create_unique(u'example_anotherexampleconfig', ['type', 'namespace'])

        # Adding model 'Article'
        db.create_table(u'example_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=234)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('section', self.gf('aldryn_apphooks_config.fields.AppHookConfigField')(to=orm['example.ExampleConfig'])),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'example', ['Article'])

        # Adding model 'News'
        db.create_table(u'example_news', (
            (u'article_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['example.Article'], unique=True, primary_key=True)),
            ('config', self.gf('aldryn_apphooks_config.fields.AppHookConfigField')(to=orm['example.AnotherExampleConfig'])),
        ))
        db.send_create_signal(u'example', ['News'])

        # Adding model 'TranslatableArticleTranslation'
        db.create_table(u'example_translatablearticle_translation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=15, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=234)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'master', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', null=True, to=orm['example.TranslatableArticle'])),
        ))
        db.send_create_signal(u'example', ['TranslatableArticleTranslation'])

        # Adding unique constraint on 'TranslatableArticleTranslation', fields ['language_code', u'master']
        db.create_unique(u'example_translatablearticle_translation', ['language_code', u'master_id'])

        # Adding model 'TranslatableArticle'
        db.create_table(u'example_translatablearticle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('aldryn_apphooks_config.fields.AppHookConfigField')(to=orm['example.ExampleConfig'])),
        ))
        db.send_create_signal(u'example', ['TranslatableArticle'])

        # Adding model 'NotApphookedModel'
        db.create_table(u'example_notapphookedmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=234)),
        ))
        db.send_create_signal(u'example', ['NotApphookedModel'])


    def backwards(self, orm):
        # Removing unique constraint on 'TranslatableArticleTranslation', fields ['language_code', u'master']
        db.delete_unique(u'example_translatablearticle_translation', ['language_code', u'master_id'])

        # Removing unique constraint on 'AnotherExampleConfig', fields ['type', 'namespace']
        db.delete_unique(u'example_anotherexampleconfig', ['type', 'namespace'])

        # Removing unique constraint on 'ExampleConfig', fields ['type', 'namespace']
        db.delete_unique(u'example_exampleconfig', ['type', 'namespace'])

        # Deleting model 'ExampleConfig'
        db.delete_table(u'example_exampleconfig')

        # Deleting model 'AnotherExampleConfig'
        db.delete_table(u'example_anotherexampleconfig')

        # Deleting model 'Article'
        db.delete_table(u'example_article')

        # Deleting model 'News'
        db.delete_table(u'example_news')

        # Deleting model 'TranslatableArticleTranslation'
        db.delete_table(u'example_translatablearticle_translation')

        # Deleting model 'TranslatableArticle'
        db.delete_table(u'example_translatablearticle')

        # Deleting model 'NotApphookedModel'
        db.delete_table(u'example_notapphookedmodel')


    models = {
        u'example.anotherexampleconfig': {
            'Meta': {'unique_together': "((u'type', u'namespace'),)", 'object_name': 'AnotherExampleConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_entries': ('django.db.models.fields.SmallIntegerField', [], {'default': '5'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'example.article': {
            'Meta': {'object_name': 'Article'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'section': ('aldryn_apphooks_config.fields.AppHookConfigField', [], {'to': u"orm['example.ExampleConfig']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '234'})
        },
        u'example.exampleconfig': {
            'Meta': {'unique_together': "((u'type', u'namespace'),)", 'object_name': 'ExampleConfig'},
            'app_data': ('app_data.fields.AppDataField', [], {'default': "'{}'"}),
            'app_title': ('django.db.models.fields.CharField', [], {'max_length': '234'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'default': 'None', 'unique': 'True', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'example.news': {
            'Meta': {'object_name': 'News', '_ormbases': [u'example.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['example.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'config': ('aldryn_apphooks_config.fields.AppHookConfigField', [], {'to': u"orm['example.AnotherExampleConfig']"})
        },
        u'example.notapphookedmodel': {
            'Meta': {'object_name': 'NotApphookedModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '234'})
        },
        u'example.translatablearticle': {
            'Meta': {'object_name': 'TranslatableArticle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('aldryn_apphooks_config.fields.AppHookConfigField', [], {'to': u"orm['example.ExampleConfig']"})
        },
        u'example.translatablearticletranslation': {
            'Meta': {'unique_together': "[(u'language_code', u'master')]", 'object_name': 'TranslatableArticleTranslation', 'db_table': "u'example_translatablearticle_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            u'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['example.TranslatableArticle']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '234'})
        }
    }

    complete_apps = ['example']