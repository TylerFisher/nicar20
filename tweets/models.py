from django.db import models


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
