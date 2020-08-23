from django.db import models

from django.urls import reverse

# Create your models here.

class Post(models.Model):
    entry_title = models.CharField(max_length=2000)
    entry_text = models.TextField()
    
    def __str__(self):
        return self.entry_title
    
    def get_absolute_url(self):
        return reverse('page-name', args=[str.self.entry_title])
    