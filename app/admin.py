from django.contrib import admin

from app.models import BlogEntry

admin.site.register(BlogEntry)

class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country', 'active']
    list_filter = ['active', 'created', 'modified']
    search_fields = ['title', 'body', 'city', 'country']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}