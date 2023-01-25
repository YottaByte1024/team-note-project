from django.contrib import admin
from .models import Note, Team


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'archived']
    list_display_links = ['name']
    list_editable = ['archived']


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'head']
    list_display_links = ['name']


admin.site.register(Note, NoteAdmin)
admin.site.register(Team, TeamAdmin)
