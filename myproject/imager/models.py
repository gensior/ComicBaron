from django.db import models
import os
from imagekit.models import ImageModel
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from myproject import settings
import random, string
import s3storage
from django.db.models.signals import post_save, post_init, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^imager\.s3storage\.S3EnabledImageField"])

import uuid
def get_file_path(instance, filename, **kwargs):
	filefolder = '%s' % (uuid.uuid4())
	filename = kwargs.get('addendum','original')
	print os.path.join('images', filefolder, filename)
	return os.path.join('images', filefolder, filename)
	
class Image(models.Model):
	image_file = s3storage.S3EnabledImageField(upload_to=get_file_path)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now = True)
	height = models.IntegerField(editable=False, default=0)
	width = models.IntegerField(editable=False, default=0)
	
	def limiter(self):
		if self.width > self.height:
			return self.width
		else:
			return self.height
			
	def save(self, force_insert=False, force_update=False):
		self.height = self.image_file.height
		self.width = self.image_file.width
		super(Image, self).save(force_insert, force_update)
	
	def __unicode__(self):
		return self.image_file.name

@receiver(post_save, sender=Image)
def tweak_imagesavepath(sender, instance, **kwargs):
	Alternates.objects.get_or_create(image=instance, limiter=instance.limiter(), width=instance.width, height=instance.height)

class Alternates(models.Model):
	image = models.ForeignKey(Image)
	limiter = models.IntegerField()
	width = models.IntegerField()
	height = models.IntegerField()
	
	def __unicode__(self):
		return u'%s %s' % (self.image.image_file.name, self.limiter)

class Page(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=100)
	filename = models.CharField(max_length=100, editable=False)
	picture = models.OneToOneField(Image, related_name='page')
	num_views = models.PositiveIntegerField(editable=False, default=0)
	published = models.BooleanField(default=True)
	parent = models.ForeignKey('self', blank=True, null=True)
	sequence = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	publish_by = models.DateTimeField(default=datetime.now)
	active = models.BooleanField(default=True)
	caption = models.CharField(max_length=255, blank=True)
	notes = models.TextField(max_length=10000, blank=True)
	
	def __unicode__(self):
		return u'%s <%s>' % (self.title, self.filename)
	
	def admin_thumbnail(self):
		return u'<img src="http://127.0.0.1:8000/image/%s/150" />' % (self.filename)
	admin_thumbnail.short_description = 'Thumbnail'
	admin_thumbnail.allow_tags = True

	def children(self):
		return self.objects.filter(parent=self.pk)
	
	"""def save(self, force_insert=False, force_update=False):
		self.image_file.name
		conn = S3Connection(AWSKEY, AWSSECRET)
		b = conn.get_all_buckets()[1]
		k = Key(b)
		k.key = self.filename
		k.set_contents_from_filename(os.path.join(BASE_DIR, 'media/images', self.image_file.name))
		super(Page, self).save(force_insert, force_update)"""
	
	"""class IKOptions:
		spec_module = 'imager.specs'
		cache_dir = 'images'
		image_field = 'image_file'
		save_count_as = 'num_views'"""

@receiver(pre_delete, sender=Page)
def remove_imagefile(sender, instance, **kwargs):
    conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(settings.DEFAULT_BUCKET)
    bucket.delete_key('images/'+instance.filename)

@receiver(post_save, sender=Page)
def tweak_imagefilename(sender, instance, **kwargs):
	post_save.disconnect(tweak_imagefilename, sender=Page)
	instance.filename = instance.picture.image_file.name.split('/')[-2]
	instance.save()
	post_save.connect(tweak_imagefilename, sender=Page)