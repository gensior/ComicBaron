from django.contrib import admin
from myproject.imager.models import Page, Image, Alternates

class ImageAdmin(admin.ModelAdmin):
	pass

class AlternatesAdmin(admin.ModelAdmin):
	pass

class PageAdmin(admin.ModelAdmin):
	list_display = ('filename', 'title', 'admin_thumbnail',)
	# inlines = [ImageInline,]

admin.site.register(Image, ImageAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Alternates, AlternatesAdmin)