from django.contrib import admin
from myproject.imager.models import Page

class PageAdmin(admin.ModelAdmin):
	list_display = ('admin_thumbnail', 'title',)

admin.site.register(Page, PageAdmin)