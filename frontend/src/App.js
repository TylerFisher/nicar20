import React from 'react';
import { connect } from 'react-redux';

import Tweet from './Tweet';

function App(props) {
  return (
    <div className="App container is-fullscreen">
      <div className="annotations">
        <h1 className="title">Tweet annotations</h1>
        {props.annotations.map(a => (
          <Tweet
            key={a.tweet.id_str}
            {...a}
          />
        ))}
      </div>
    </div>
  );
}

const mapStateToProps = state => {
  return {
    annotations: state.annotations,
    tweets: state.tweets,
  }
};

export default connect(mapStateToProps)(App);
