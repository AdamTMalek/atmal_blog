from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import PostTranslations


admin.site.register(PostTranslations, MarkdownxModelAdmin)
