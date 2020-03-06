import { composeWithDevTools } from 'redux-devtools-extension';
import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk';

import annotations from './annotations/reducers';

const reducers = combineReducers({
  annotations,
});

const middleware = [thunkMiddleware];
const middlewareEnhancer = applyMiddleware(...middleware);
const store = createStore(reducers, composeWithDevTools(middlewareEnhancer));

export default store;
