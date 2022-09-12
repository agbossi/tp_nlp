from rest_framework import serializers

from tp_nlp_app.models import Place, Summary, Review


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'rate', 'id']


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['placeId', 'good', 'bad', 'neutral']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['placeId', 'text']