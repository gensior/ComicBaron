from django.contrib import admin
from myproject.imager.models import Page

class PageAdmin(admin.ModelAdmin):
	pass

admin.site.register(Page, PageAdmin)