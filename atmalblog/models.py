from django.db import models


class Language(models.Model):
    """
    Stores languages that are used in the blog
    """
    code = models.CharField(max_length=2)  # ISO-639-1 code
    native_name = models.CharField(max_length=20)


class Category(models.Model):
    """
    Represents different post categories such as AVR, C, etc.
    These names are expected to be universal to all languages.
    """
    name = models.CharField(max_length=15)


class Series(models.Model):
    """
    Represents a series of posts.
    These will be used, for instance, to group together posts that were originally split due to their length.
    """
    pass  # This table will just hold the ID of the series.


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
    content = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    published_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'language'], name='unique_post_translation')
        ]
