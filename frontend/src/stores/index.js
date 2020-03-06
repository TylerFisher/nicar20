import { composeWithDevTools } from 'redux-devtools-extension';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk';

import annotations from './annotations/reducers';
import { fetchAnnotations } from './annotations/api';

import tweets from './tweets/reducers';
import { fetchTweets } from './tweets/api';

const reducers = combineReducers({
  annotations,
  tweets
});

const middleware = [thunkMiddleware];
const middlewareEnhancer = applyMiddleware(...middleware);
const store = createStore(reducers, composeWithDevTools(middlewareEnhancer));

store.dispatch(fetchAnnotations());
store.dispatch(fetchTweets());

export default store;
