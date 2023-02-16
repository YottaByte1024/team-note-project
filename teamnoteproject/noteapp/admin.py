from django.contrib import admin
from .models import Note, Post, Team


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team', 'archived']
    list_display_links = ['name']
    list_editable = ['archived']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'head']
    list_display_links = ['name']


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_published', 'priority']
    list_display_links = ['name']
    list_editable = ['is_published', 'priority']


admin.site.register(Note, NoteAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Post, PostAdmin)
