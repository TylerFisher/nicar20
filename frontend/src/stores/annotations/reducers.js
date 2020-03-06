import * as types from './constants';

export default (currentState, action) => {
  const initialState = [];
  if (typeof currentState === "undefined") {
    return initialState;
  }

  switch(action.type) {
    case types.UPSERT_ANNOTATIONS:
      return action.annotations;
    default:
      break;
  }

  return currentState;
}
