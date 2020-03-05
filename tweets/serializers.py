from rest_framework import serializers
from tweets.models import Tweet, Annotation


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"


class AnnotationSerializer(serializers.ModelSerializer):
    tweet = serializers.SerializerMethodField()

    def get_tweet(self, obj):
        return TweetSerializer(obj.tweet).data

    class Meta:
        model = Annotation
        fields = ["tweet", "annotation", "author"]
