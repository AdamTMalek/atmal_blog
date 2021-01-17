from django.forms import *
from markdownx.fields import MarkdownxFormField

from atmalblog.models import *


class PostForm(Form):
    categories = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                          required=(not Post._meta.get_field('categories').blank))
    series = ModelChoiceField(queryset=Series.objects.all(),
                              empty_label="(No series)",
                              required=(not Post._meta.get_field('series').blank))
    thumbnail = ImageField(required=(not Post._meta.get_field('thumbnail').blank))
    title = CharField(max_length=PostTranslations._meta.get_field('title').max_length,
                      required=(not PostTranslations._meta.get_field('title').blank))
    short_description = CharField(max_length=PostTranslations._meta.get_field('short_description').max_length,
                                  required=(not PostTranslations._meta.get_field('short_description').blank))
    content = MarkdownxFormField()
    language = ModelChoiceField(queryset=Language.objects.all(), empty_label="(Choose a language)",
                                required=(not PostTranslations._meta.get_field('language').blank))


class SeriesTranslationForm(Form):
    name = CharField(max_length=SeriesTranslations._meta.get_field('name').max_length)
    language = CharField(max_length=SeriesTranslations._meta.get_field('language').max_length)


SeriesTranslationFormSet = formset_factory(SeriesTranslationForm, extra=0)


class CategoryTranslationForm(Form):
    name = CharField(max_length=CategoryTranslation._meta.get_field('name').max_length)
    language = CharField(max_length=CategoryTranslation._meta.get_field('language').max_length)


CategoryTranslationFormSet = formset_factory(CategoryTranslationForm, extra=0)
