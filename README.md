
# How to build a data-driven app that never goes down

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


##### Step two: Set up signals for publishing live data

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

##### Step three: Set up our frontend to accept the data

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

##### Step four: make it live!

To make this app truly "live", it needs to download the data more than on page load. This way, people don't have to refresh to get new data. In `frontend/src/stores/index.js`, above the last line, add the following:

```
setTimeout(() => {
  store.dispatch(fetchAnnotations())
}, 5000);
```

That's it, we're done!
e render function, that looks like this:

```
constructor(props) {
  super(props);

  this.state = {
    currentBody: 'senate',
  };
}
```

Next, we're going to use this state to filter the offices that we are showing. Add the following to the top of the render function:

```
const filteredOffices = this.props.offices.filter(office => office.body.slug === this.state.currentBody);
```

Then, change lines 34-36 to read:

```
{filteredOffices.map(office => (
  <Row office={office} key={office.id} />
))}
```

Our button still doesn't do anything. It needs an event listener for clicks, so that it can change the state. First, let's write the function. Add this below the constructor:

```
changeBody() {
  this.setState({
    currentBody: this.state.currentBody === 'senate' ? 'house' : 'senate',
  });
}
```

Then, add an `onClick` handler to our button:

```
<button onClick={this.changeBody}>Change body</button>
```

Oops, this actually errors out. We need to add one more thing to our constructor so that our change function has the ability to change the component's state:

```
this.changeBody = this.changeBody.bind(this);
```

Now try your button. It works! We're done!
