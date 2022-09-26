from django.db import models
from django.utils import timezone
from django.urls.base import reverse

from businesswebsite.settings import BASE_DIR

class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class KnowledgeBaseCategory(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class KnowledgeBaseEntry(models.Model):
    slug = models.SlugField(max_length=255, help_text="A unique slug used in the url.", default="slooog", unique=True)
    # Entry title
    short_title = models.CharField(max_length=50, help_text="A short title for display on small devices. 50 characters.")
    medium_title = models.CharField(max_length=100, help_text="A medium length title for display on medium devices. 100 characters.")
    # Description
    short_description = models.TextField(help_text="A short description for display on small devices. 500 characters.", default="Knowledge base entry short description", max_length=500)
    # The content
    entry = models.TextField(help_text="A markdown embellished entry for the this knowledge base topic. 10000 characters. About 2000 words.", default="Knowledge base entry", max_length=10000)
    # A category
    category = models.ForeignKey(KnowledgeBaseCategory, on_delete=models.SET_NULL, null=True, blank=True, help_text="ID of the appropriate category")

    author = models.CharField(max_length=40, default="Uknown Author", help_text="The author of this article.")
    #pub_date = models.DateField(auto_now_add=True)
    #last_edited = AutoDateTimeField(default=timezone.localdate)
    draft = models.BooleanField(default=True, help_text="Set to true when the article is being drafted, set to false when you want to be published. This feature is only used by the sitemap builder to ensure articles under construction aren't listed as crawlable by robots.")

    def get_absolute_url(self):
        return reverse("article", kwargs={"slug": self.slug})    

    def __str__(self):
        return self.medium_title

class FAQEntry(models.Model):
    # Title
    title = models.CharField(max_length=50, help_text="A title in question format. Full length. 50 characters.") 
    # Entry
    entry = models.TextField(help_text="A markdown embellished entry for the this FAQ question. 5000 characters.", max_length=5000)
    pub_date = models.DateField(default=timezone.localdate)

    def get_absolute_url(self):
        return reverse("faq", args="#%s"%self.title)   

    def __str__(self):
        return self.title