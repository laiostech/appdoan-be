from django.contrib import admin
from .models import News, Reaction

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'create_at', 'update_at']
    list_filter = ['category', 'create_at']
    search_fields = ['title', 'content']
    readonly_fields = ['id', 'create_at', 'update_at']

@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news']
    list_filter = ['news'] 