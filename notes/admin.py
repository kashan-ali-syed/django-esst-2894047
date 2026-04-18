from django.contrib import admin
from . import models

class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'text')
    ordering = ('created_at',)

admin.site.register(models.Notes, NotesAdmin)