from django.contrib import admin

# Register your models here.

from .models import Comment, News, Topic

admin.site.register(News)
admin.site.register(Topic)
admin.site.register(Comment)
