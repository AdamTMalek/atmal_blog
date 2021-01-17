from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.apps import apps
from markdownx.admin import MarkdownxModelAdmin
from .models import *


admin.site.register(PostTranslations, MarkdownxModelAdmin)

models = apps.get_app_config('atmalblog').get_models()
for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
