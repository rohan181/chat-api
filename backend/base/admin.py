from django.contrib import admin

# Register your models here.

from .models import Note,video
admin.site.register(Note)
admin.site.register(video)
