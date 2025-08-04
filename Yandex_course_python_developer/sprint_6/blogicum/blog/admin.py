from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'category__title', 'location__name', 'author')
    list_filter = ('author', 'is_published', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
