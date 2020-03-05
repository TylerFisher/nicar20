from django.contrib.auth.models import User
from rest_framework import serializers
from tweets.models import Tweet, Annotation


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class AnnotationSerializer(serializers.ModelSerializer):
    tweet = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    def get_tweet(self, obj):
        return TweetSerializer(obj.tweet).data

    def get_author(self, obj):
        return UserSerializer(obj.author).data

    class Meta:
        model = Annotation
        fields = ["tweet", "annotation", "author", "publish_date"]
