#-* coding:utf-8 -*-
from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30,blank=True)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title
        