from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import *


admin.site.register(PostTranslations, MarkdownxModelAdmin)
admin.site.register(Language)
