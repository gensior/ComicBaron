from django.http import HttpResponse
from myproject.imager.models import Page, Image
from PIL import Image
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from myproject import settings
import os

def serveimage(request, imagefile, resolution=0):
	resolution = int(resolution)
	page = Page.objects.get(filename=imagefile)
	limiter = int(page.picture.limiter())
	print limiter
	if resolution:
		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.DEFAULT_BUCKET)
		k = Key(bucket, page.picture.image_file.name)
		k.get_contents_to_filename(os.path.join(settings.BASE_DIR, 'media/images/tmp'))
		i = Image.open(os.path.join(settings.BASE_DIR, 'media/images/tmp'))
		filename = str(imagefile) + "_" + str(resolution)
		if resolution < limiter:
			ratio = float(resolution)/float(limiter)
			width = int(float(page.picture.width) * float(ratio))
			height = int(float(page.picture.height) * float(ratio))
			i = i.resize((width, height))
	else:
		filename = str(imagefile)
	response = HttpResponse(mimetype="image/png")
	i.save(response, "PNG")
	return response