from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    source = models.CharField(max_length=140)
    id_str = models.CharField(max_length=50)
    text = models.TextField()
    created_at = models.DateTimeField()
    retweet_count = models.IntegerField()
    in_reply_to_user_id_str = models.CharField(
        max_length=50, null=True, blank=True
    )
    favorite_count = models.IntegerField()
    is_retweet = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Annotation(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    annotation = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Annotation: " + self.tweet.text
