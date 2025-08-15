import React from 'react';
import VideoList from '../components/VideoList';

const Videos = () => {
  return (
    <div className="videos-page">
      <h1>Your Generated Videos</h1>
      <VideoList />
    </div>
  );
};

export default Videos;