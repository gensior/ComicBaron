from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from myproject.imager.models import Page, Image as djangoimage, Alternates
from PIL import Image
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from myproject import settings
import os
from django.contrib.auth.models import User
from datetime import datetime

def index(request):
	try:
		user = User.objects.filter(username=str(request.subdomain))[0]
		pages = Page.objects.filter(author=user.id, published=True, active=True, publish_by__lte=datetime.now).order_by('-publish_by')
	except AttributeError:
		user = False
		pages = Page.objects.filter(published=True, active=True, publish_by__lte=datetime.now).order_by('-publish_by')
	return render(request, 'index.html', {'pages': pages, 'user': user }, )

def read(request, page):
	page = get_object_or_404(Page, pk=page)
	page.num_views += 1
	page.save()
	return render(request, 'read.html', {'page': page }, )

def serveimage(request, imagefile, resolution=0):
	### can the image file be found?
	original = 0
	page = Page.objects.get(filename=imagefile)
	imageobject = djangoimage.objects.get(id=page.picture.id)
	limiter = int(imageobject.limiter())
	if resolution:
		resolution = int(resolution)
		if resolution > limiter:
			resolution = limiter
			original = 1
	else:
		resolution = limiter
		original = 1
	### does an alternate already exist?
	try:
		alternate = Alternates.objects.get(image=imageobject, limiter=resolution)
		if resolution == limiter:
			resolution = 'original'
		return HttpResponseRedirect('https://s3.amazonaws.com/imagebaron/images/'+page.filename+'/'+str(resolution))
	except Alternates.DoesNotExist:
		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		bucket = conn.get_bucket(settings.DEFAULT_BUCKET)
		k1 = Key(bucket, 'images/'+page.filename+'/'+'original')
		k1.get_contents_to_filename(os.path.join(settings.BASE_DIR, 'media/images/tmp'))
		k = Key(bucket, 'images/'+page.filename+'/'+str(resolution))
		i = Image.open(os.path.join(settings.BASE_DIR, 'media/images/tmp'))
		if resolution < limiter:
			ratio = float(resolution)/float(limiter)
			width = int(float(page.picture.width) * float(ratio))
			height = int(float(page.picture.height) * float(ratio))
			i = i.resize((width, height))
			Alternates.objects.get_or_create(image=imageobject, limiter=resolution, width=width, height=height)
		i.save(os.path.join(settings.BASE_DIR, 'media/images/tmp'), "PNG")
		k.set_metadata('Content-Type', 'image/png')
		k.set_contents_from_filename(os.path.join(settings.BASE_DIR, 'media/images/tmp'))
		k.make_public()
		return HttpResponseRedirect('https://s3.amazonaws.com/imagebaron/images/'+page.filename+'/'+str(resolution))