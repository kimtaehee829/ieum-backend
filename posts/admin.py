from django.contrib import admin
from .models import Post, Clue, Tag

admin.site.register(Post)
admin.site.register(Clue)
admin.site.register(Tag)