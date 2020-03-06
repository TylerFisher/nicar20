import React from 'react';

function Annotation(props) {
  console.log(props);
  return (
    <article className="media">
      <figure className="media-left">
        <p className="image is-48x48">
          <img src="https://bulma.io/images/placeholders/96x96.png" alt="Placeholder" />
        </p>
      </figure>
      <div className="media-content">
        <div className="content">
          <p className="title is-4">{props.author.first_name} {props.author.last_name}</p>
          <p className="subtitle is-6">{props.author.email}</p>
          <p>{props.annotation}</p>
         </div>
       </div>
    </article>
  )
}

export default Annotation;
