import React, { useState } from 'react';
import VideoForm from '../components/VideoForm';
import VideoPlayer from '../components/VideoPlayer';

const Home = () => {
  const [generatedVideo, setGeneratedVideo] = useState(null);

  const handleVideoGenerated = (videoPath) => {
    setGeneratedVideo(videoPath);
  };

  return (
    <div className="home-page">
      <h1>Text to Video Generator</h1>
      <p>Enter a prompt to generate a video using AI</p>
      
      <div className="content-wrapper">
        <div className="form-section video-section">
          <VideoForm onVideoGenerated={handleVideoGenerated} />
        
          <VideoPlayer videoPath={generatedVideo} />
        </div>
      </div>
    </div>
  );
};

export default Home;