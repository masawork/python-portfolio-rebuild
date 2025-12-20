from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import markdown


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body_markdown = models.TextField(help_text="Markdown形式で記述")
    summary = models.TextField(blank=True)
    tags = models.ManyToManyField('portfolio.Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def get_body_html(self):
        return markdown.markdown(self.body_markdown, extensions=['extra', 'codehilite'])

