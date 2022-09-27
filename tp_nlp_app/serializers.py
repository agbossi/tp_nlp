from rest_framework import serializers

from tp_nlp_app.models import Place, Summary, Review, BlacklistedWord


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'rate', 'latitude', 'longitude', 'placeId']


class PlaceInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['name', 'latitude', 'longitude']


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = '__all__'


class ResponseSummarySerializer(serializers.Serializer):
    summary = SummarySerializer()
    goodImgUrl = serializers.CharField()
    badImgUrl = serializers.CharField()
    neutralImgUrl = serializers.CharField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['placeId', 'text', 'date', 'rating', 'likes', 'reviewId']


class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistedWord
        fields = ['word']
