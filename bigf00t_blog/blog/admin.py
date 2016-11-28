from django.contrib import admin

from .models import PostModel, ImageModle, CategoriesModel


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'updatetime', 'createtime', 'publishtime']
    list_display_links = ['title', 'updatetime', 'createtime', 'publishtime']
    list_filter = ['updatetime', 'category', 'createtime', 'publishtime']
    search_fields = ['title', 'category', 'content']


class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['post', 'image']
    list_display_links = ['post']
    search_fields = ['image']


class CategorieModelAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(PostModel, PostModelAdmin)
admin.site.register(ImageModle, ImageModelAdmin)
admin.site.register(CategoriesModel, CategorieModelAdmin)
