from tkinter import W
from django.contrib.sitemaps import Sitemap
from django.urls.base import reverse
from .models import KnowledgeBaseEntry, FAQEntry
from businesswebsite.settings import SITEMAP_DEFAULT_LAST_MOD

class ArticleSitemap(Sitemap):
    protocol = "https"
    changefreq = "never"
    priority = 0.5

    def items(self):
        return KnowledgeBaseEntry.objects.filter(draft=False)

    def lastmod(self, obj):
        return obj.last_edited

class StaticViewSitemap(Sitemap):
    protocol = "https"
    changefreq = "never"
    priority = 0.5

    def location(self, item):
        return reverse(item)

    def items(self):
        return ['services', 'about', 'school', 'faq']

    


