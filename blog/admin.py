from django.contrib import admin

from blog.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display= ('title', 'slug','author', 'content','preview', 'date_create','is_published', 'count_views',)
    list_filter = ('title','is_published',)
    search_fields = ('title','author',)
