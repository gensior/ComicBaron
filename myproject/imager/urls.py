from django.conf.urls.defaults import *

urlpatterns = patterns('imager.views',
	(r'(?P<imagefile>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/(?P<resolution>\d+)$', 'serveimage'),
)