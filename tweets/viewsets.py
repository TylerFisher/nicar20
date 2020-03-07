from rest_framework import viewsets
from tweets.models import Tweet, Annotation
from tweets.serializers import TweetSerializer, AnnotationSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
