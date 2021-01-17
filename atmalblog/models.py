from django.db import models
from markdownx import models as markdownx_models


class Language(models.Model):
    """
    Stores languages that are used in the blog
    """
    code = models.CharField(max_length=2, primary_key=True, help_text='ISO-639-1 code')  # ISO-639-1 code
    native_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.native_name


class Category(models.Model):
    """
    Represents different post categories such as AVR, C, etc.
    """
    pass

    def __str__(self):
        return "/".join([x.name for x in CategoryTranslation.objects.filter(category=self.pk)])


class CategoryTranslation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['category', 'language'], name='unique_category_translation')
        ]


class Series(models.Model):
    """
    Represents a series of posts.
    These will be used, for instance, to group together posts that were originally split due to their length.
    """
    pass

    def __str__(self):
        translations = "/".join([x.name for x in SeriesTranslations.objects.filter(series=self.pk)])
        return translations


class SeriesTranslations(models.Model):
    """
    Holds the translated series title
    """
    series = models.ForeignKey(Series, on_delete=models.PROTECT)
    name = models.CharField(max_length=25)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['series', 'language'], name='unique_series_translation')
        ]


class Post(models.Model):
    """
    Represents a single post which can have multiple categories and belong to a series.
    """
    categories = models.ManyToManyField(Category)
    series = models.ForeignKey(Series, on_delete=models.PROTECT, blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/')


class PostTranslations(models.Model):
    """
    Holds the language-dependent post parts, such as its title and content.
    """
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=275)
    content = markdownx_models.MarkdownxField()
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    published_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'language'], name='unique_post_translation')
        ]
