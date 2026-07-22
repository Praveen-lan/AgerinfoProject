from django.contrib import admin
from .models import News, Gallery, Slider, Topic


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('caption', 'created_at')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'created_at')
    search_fields = ('title', 'description')
