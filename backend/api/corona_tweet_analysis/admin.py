from django.contrib import admin
from corona_tweet_analysis.models import Category, TwitterData, CoronaReport

admin.site.register(Category)
admin.site.register(TwitterData)
admin.site.register(CoronaReport)
