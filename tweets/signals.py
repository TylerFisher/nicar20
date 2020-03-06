import json
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from tweets.models import Tweet, Annotation
from tweets.serializers import TweetSerializer, AnnotationSerializer


@receiver(post_save, sender=Tweet)
def publish_recent_tweets(sender, instance, **kwargs):
    cmd_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(cmd_path, "../frontend/public/data/")
    recent_tweets = Tweet.objects.all().order_by("-created_at")[:50]
    serialized = TweetSerializer(recent_tweets, many=True).data

    with open(os.path.join(data_path, "recent-tweets.json"), 'w') as f:
        json.dump(serialized, f)


@receiver(post_save, sender=Annotation)
def publish_annotations(sender, instance, **kwargs):
    print("running signal")
    cmd_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(cmd_path, "../frontend/public/data/")
    annotations = Annotation.objects.all()
    serialized = AnnotationSerializer(annotations, many=True).data

    with open(os.path.join(data_path, "annotations.json"), 'w') as f:
        json.dump(serialized, f)
