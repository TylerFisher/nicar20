import * as actions from './actions';

export const fetchTweets = () =>
  dispatch => fetch('/data/recent-tweets.json', { method: "GET" })
    .then(response => response.json())
    .then(data => Promise.all([dispatch(actions.upsertTweets(data))]))
    .catch(error => {
      console.error("API Error fetchTweets", error, error.code)
    });
