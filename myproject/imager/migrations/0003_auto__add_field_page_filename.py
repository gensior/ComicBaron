# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Page.filename'
        db.add_column('imager_page', 'filename', self.gf('django.db.models.fields.CharField')(default='bleh', max_length=100), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Page.filename'
        db.delete_column('imager_page', 'filename')


    models = {
        'imager.page': {
            'Meta': {'object_name': 'Page'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'num_views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['imager']
