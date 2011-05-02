from django.db import models
from imagekit.models import ImageModel

class Page(ImageModel):
	title = models.CharField(max_length=100)
	image_file = models.ImageField(upload_to="images")
	num_views = models.PositiveIntegerField(editable=False, default=0)
	
	class IKOptions:
		spec_module = 'imager.specs'
		cache_dir = 'images'
		image_field = 'image_file'
		save_count_as = 'num_views'