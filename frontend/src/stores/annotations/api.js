import * as actions from './actions';

export const fetchAnnotations = () =>
  dispatch => fetch('/data/annotations.json', { method: "GET" })
    .then(response => response.json())
    .then(data => Promise.all([dispatch(actions.upsertAnnotations(data))]))
    .catch(error => {
      console.error("API Error fetchAnnotations", error, error.code)
    });
