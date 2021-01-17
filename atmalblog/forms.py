from django.forms import *
from markdownx.fields import MarkdownxFormField

from atmalblog.models import *


class OriginalPostForm(ModelForm):
    class Meta:
        model = PostTranslations
        fields = ['title', 'short_description', 'language', 'content']


class PostForm(Form):
    categories = ModelMultipleChoiceField(queryset=Category.objects.all(),
                                          required=(not Post._meta.get_field('categories').blank))
    series = ModelChoiceField(queryset=Series.objects.all(),
                              empty_label="(No series)",
                              required=(not Post._meta.get_field('series').blank))
    thumbnail = ImageField(required=(not Post._meta.get_field('thumbnail').blank))
    title = CharField(max_length=PostTranslations._meta.get_field('title').max_length)
    short_description = CharField(max_length=PostTranslations._meta.get_field('short_description').max_length)
    content = MarkdownxFormField()
    language = ModelChoiceField(queryset=Language.objects.all(), empty_label="(Choose a language)")


class SeriesTranslationForm(Form):
    name = CharField(max_length=SeriesTranslations._meta.get_field('name').max_length)
    language = CharField(max_length=SeriesTranslations._meta.get_field('language').max_length)


SeriesTranslationFormSet = formset_factory(SeriesTranslationForm, extra=0)
