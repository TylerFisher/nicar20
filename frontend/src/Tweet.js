import React from 'react';
import Annotation from './Annotation';

function Tweet(props) {
  return (
    <article className="media">
      <div className="media-left">
        <figure className="image is-48x48">
          <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder" />
        </figure>
      </div>
      <div className="media-content">
        <div className="content">
          <p className="title is-4">Donald J. Trump</p>
          <p className="subtitle is-6">@realdonaldtrump</p>
          <p>{props.tweet.text}</p>
        </div>
        {props.annotation ? (
          <Annotation annotation={props.annotation} author={props.author} />
        ) : (
          <div />
        )}
      </div>
    </article>
  )
}

export default Tweet;
