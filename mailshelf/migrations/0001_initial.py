# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Message'
        db.create_table('mailshelf_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('mailshelf', ['Message'])

        # Adding model 'MessageItem'
        db.create_table('mailshelf_messageitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailshelf.Message'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('body_text', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
            ('locale', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=5)),
        ))
        db.send_create_signal('mailshelf', ['MessageItem'])


    def backwards(self, orm):
        
        # Deleting model 'Message'
        db.delete_table('mailshelf_message')

        # Deleting model 'MessageItem'
        db.delete_table('mailshelf_messageitem')


    models = {
        'mailshelf.message': {
            'Meta': {'object_name': 'Message'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'mailshelf.messageitem': {
            'Meta': {'object_name': 'MessageItem'},
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locale': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '5'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailshelf.Message']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['mailshelf']
