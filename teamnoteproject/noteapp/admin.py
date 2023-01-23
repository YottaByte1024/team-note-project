from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'archived']
    list_display_links = ['id', 'name']
    list_editable = ['archived']


admin.site.register(Note, NoteAdmin)
