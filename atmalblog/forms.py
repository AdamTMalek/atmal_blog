from django.forms import Form, formset_factory, CharField

from atmalblog.models import *


class SeriesTranslationForm(Form):
    name = CharField(max_length=SeriesTranslations._meta.get_field('name').max_length)
    language = CharField(max_length=SeriesTranslations._meta.get_field('language').max_length)


SeriesTranslationFormSet = formset_factory(SeriesTranslationForm, extra=0)
