from django.db import models
from imagekit.models import ImageModel

class Page(ImageModel):
	title = models.CharField(max_length=100)
	image_file = models.ImageField(upload_to="images")
	num_views = models.PositiveIntegerField(editable=False, default=0)
	
	def __unicode__(self):
		return u'%s' % (self.title)
	
	def admin_thumbnail(self):
		return u'<img src="http://127.0.0.1:8000/static/images/%s" />' % (self.image_file.url)
	admin_thumbnail.short_description = 'Thumbnail'
	admin_thumbnail.allow_tags = True
	
	class IKOptions:
		spec_module = 'imager.specs'
		cache_dir = 'images'
		image_field = 'image_file'
		save_count_as = 'num_views'