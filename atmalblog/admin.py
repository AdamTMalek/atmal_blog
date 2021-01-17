from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from markdownx.admin import *

from .models import *


@admin.register(PostTranslations)
class PostTranslationAdmin(admin.ModelAdmin):
    fields = ('post', 'title', 'short_description', 'language')
    list_display = ('post', 'title', 'short_description', 'published_date')


models = apps.get_app_config('atmalblog').get_models()
for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
