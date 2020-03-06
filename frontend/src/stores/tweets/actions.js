import * as types from './constants';

export function upsertTweets(tweets) {
  return {
    type: types.UPSERT_TWEETS,
    tweets: tweets,
  };
};
