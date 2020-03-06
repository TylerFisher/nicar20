import * as types from './constants';

export function upsertAnnotations(annotations) {
  return {
    type: types.UPSERT_ANNOTATIONS,
    annotations: annotations,
  };
};
