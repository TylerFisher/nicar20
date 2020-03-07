
# How to build a data-driven app that never goes down

[Slides](https://docs.google.com/presentation/d/16iYbBlPa2pOwUjRTKzUT2siucrSCNIUzdyFcU_A0kVg/edit#slide=id.p)

### Quickstart

First, install requirements and load data

```
$ pipenv install
$ pipenv run python manage.py migrate
$ pipenv run python manage.py load_tweets
$ cd frontend
$ npm install
$ python manage.py createsuperuser
```

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server. Note that you need the Python server running in a separate tab.

  ```
  $ cd frontend
  $ npm start
  ```

## The class!

##### What are we doing

We're going to build a backend that publishes live data (annotations of Donald Trump's twitter feed), and a frontend that accepts it.

##### What we need to do

We need to:

- Build JSON serializers for our models
- Set up signals for publishing live data
- Add viewsets for our API
- Set up our frontend to accept the data
- Make it live!

##### Step one: Build JSON serializers for our models

First, we need to build a JSON serializer for our three models, `Tweet`, `Annotation`, and `User`. We use Django Rest Framework to create our serializers, like this:

```
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
```

##### Step two: Add viewsets for our API

Next, we'll add viewsets for our API. This allows us to explore the API from the browser.

First, create the viewsets in `tweets/viewsets.py`:

```
from rest_framework import viewsets
from tweets.models import Tweet, Annotation
from tweets.serializers import TweetSerializer, AnnotationSerializer


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
```

Then, attach URLs to your viewsets by writing the following in `tweets/urls.py`.

```
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TweetViewSet, AnnotationViewSet

router = DefaultRouter()
router.register(r'tweets', TweetViewSet)
router.register(r'annotations', AnnotationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Finally, attach your tweets app to the Django project's main URL config in `config/urls.py`.

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', include('tweets.urls'))
]
```

Visit `localhost:8000/tweets/api` to start exploring your API.

##### Step three: Set up signals for publishing live data

Next, we'll create Django signals. Signals are functions that fire automatically when specific things happen in Django. For our purposes, we want to publish JSON every time something changes in our database.

We need to do a couple things to set up Django signals. Edit `tweets/__init__.py` to look like this:

```
default_app_config = 'tweets.apps.TweetsConfig'
```

And edit `tweets/apps.py` to look like this:

```
from django.apps import AppConfig


class TweetsConfig(AppConfig):
    name = 'tweets'

    def ready(self):
        from tweets import signals
```

Finally, we're ready to write our signals. Edit your `tweets/signals.py` file to look like this:

```
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
```

Go into the Django admin at `localhost:8000/admin`, and create an annotation. You should see a JSON file at `frontend/public/annotations.json`.


##### Step four: Set up our frontend to accept the data

To get the data to React, we need to set up a fetch request that will get the data we just published from our signals. In `frontend/src/stores/annotations/api.js`, add the following:

```
import * as actions from './actions';

export const fetchAnnotations = () =>
  dispatch => fetch('/data/annotations.json', { method: "GET" })
    .then(response => response.json())
    .then(data => Promise.all([dispatch(actions.upsertAnnotations(data))]))
    .catch(error => {
      console.error("API Error fetchAnnotations", error, error.code)
    });
```

Now, we need to call this function. We do that in `frontend/src/stores/index.js`. Replace the current file with this:

```
import { composeWithDevTools } from 'redux-devtools-extension';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk';

import annotations from './annotations/reducers';
import { fetchAnnotations } from './annotations/api';

const reducers = combineReducers({
  annotations,
});

const middleware = [thunkMiddleware];
const middlewareEnhancer = applyMiddleware(...middleware);
const store = createStore(reducers, composeWithDevTools(middlewareEnhancer));

store.dispatch(fetchAnnotations());

export default store;
```

##### Step five: make it live!

To make this app truly "live", it needs to download the data more than on page load. This way, people don't have to refresh to get new data. In `frontend/src/stores/index.js`, above the last line, add the following:

```
setInterval(() => {
  store.dispatch(fetchAnnotations())
}, 5000);
```

That's it, we're done!
