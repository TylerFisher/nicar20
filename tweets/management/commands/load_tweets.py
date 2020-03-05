import json
import os

from datetime import datetime
from django.core.management.base import BaseCommand
from tweets.models import Tweet


class Command(BaseCommand):
    def upsert_tweets(self, data):
        for tweet in data:
            Tweet.objects.get_or_create(
                source=tweet["source"],
                id_str=tweet["id_str"],
                text=tweet["text"],
                created_at=datetime.strptime(
                    tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y"
                ),
                retweet_count=tweet["retweet_count"],
                in_reply_to_user_id_str=tweet["in_reply_to_user_id_str"],
                favorite_count=tweet["favorite_count"],
                is_retweet=tweet["is_retweet"]
            )

    def handle(self, *args, **options):
        cmd_path = os.path.dirname(os.path.realpath(__file__))
        data_path = os.path.join(cmd_path, "../../../data/")

        for file in os.listdir(data_path):
            with open(os.path.join(data_path, file)) as f:
                data = json.load(f)
                self.upsert_tweets(data)
