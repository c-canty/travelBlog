from django.contrib import admin

from app.models import BlogEntry, Trip, TripComment, NewsFeedEntry, TripPhoto

admin.site.register(BlogEntry)

class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country', 'active']
    list_filter = ['active', 'created', 'modified']
    search_fields = ['title', 'body', 'city', 'country']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Trip)
admin.site.register(TripComment)
admin.site.register(NewsFeedEntry)
admin.site.register(TripPhoto)

class TripAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'active']
    list_filter = ['active', 'created', 'modified']
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}

class TripCommentAdmin(admin.ModelAdmin):
    list_display = ['trip', 'comment', 'author']
    list_filter = ['trip', 'created', 'modified']
    search_fields = ['comment']
    date_hierarchy = 'created'
    save_on_top = True

class NewsFeedEntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active', 'created', 'modified']
    search_fields = ['title', 'body']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}

class TripPhotoAdmin(admin.ModelAdmin):
    list_display = ['trip', 'imageLink']
    list_filter = ['trip', 'created', 'modified']
    search_fields = ['imageLink']
    date_hierarchy = 'created'
    save_on_top = True
    prepopulated_fields = {'slug': ('title',)}
# Register your models here.