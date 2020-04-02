from rest_framework import serializers
from  corona_tweet_analysis.models import TwitterData, Category, CoronaReport


class TwitterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterData
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CoronaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoronaReport
        fields = '__all__'

