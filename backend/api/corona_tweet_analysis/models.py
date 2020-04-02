import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Category(models.Model):
    _id = models.CharField(primary_key=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self._id


class TwitterData(models.Model):
    text = models.TextField()
    country = ArrayField(models.CharField(max_length=50),default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    category = ArrayField(models.CharField(max_length=50), default=list)
    hashtags = ArrayField(models.CharField(max_length=100), default=list)
    spam_count = models.IntegerField(default=0)
    is_spam = models.BooleanField(default=False)
    spam_users = ArrayField(models.CharField(max_length=50), default=list)
    url = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'TwitterData'
        verbose_name_plural = 'TwitterData'
    

# class Data(models.Model):
#     name = models.CharField(max_length=100)
#     new_cases = models.CharField(max_length=100)
#     new_deaths = models.CharField(max_length=100)
#     total_cases = models.CharField(max_length=100)
#     total_deaths = models.CharField(max_length=100)


class CoronaReport(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    data = JSONField()
